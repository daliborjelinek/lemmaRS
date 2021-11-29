import arrow
from django.core.mail import send_mail
from django.utils import timezone

from rs.models import User, PermissionRequest, Reservation


class Mailer:
    # Admin notification about new reservation which needs to be approved
    @staticmethod
    def send_reservation_approval_request_email(reservation):
        recipients = list(
            User.objects.filter(send_notification_on_reservation_request=True).values_list('email', flat=True))
        message = f"""V rezervačním systému byla vytvořena nová rezervace, která vyžaduje schválení.
             OD: {arrow.get(reservation.pickup_date_time).format('DD. MM. YYYY HH:mm')}
             DO: {arrow.get(reservation.return_date_time).format('DD. MM. YYYY HH:mm')}"""

        send_mail(
            '🎥 RS LEMMA: Požadavek na schválení rezervace',
            message,
            None,
            recipients,
            fail_silently=False,
        )

    # Provider notification about new reservation.
    @staticmethod
    def send_new_reservation_email(reservation):
        print(reservation)
        message = f"""V rezervačním systému byla vytvořena nová rezervace zdrojů ve vaší správě.
        OD: {arrow.get(reservation.pickup_date_time).format('DD. MM. YYYY HH:mm')}
        DO: {arrow.get(reservation.return_date_time).format('DD. MM. YYYY HH:mm')}"""

        send_mail(
            '🎥 RS LEMMA: Nová rezervace',
            message,
            None,
            [reservation.provider.email],
            fail_silently=False,
        )

    # Admin notification about new permission request
    @staticmethod
    def send_new_permission_request_email(pr):
        recipients = list(
            User.objects.filter(send_notification_on_permission_request=True).values_list('email', flat=True))
        message = f"""Uživatel {pr.applicant.fullname} žádá oprávnění {pr.requested_level.name} z následujícího důvodu: {pr.reason}"""
        send_mail(
            '🎥 RS LEMMA: Nová žádost o operávnění',
            message,
            None,
            recipients,
            fail_silently=False,
        )

    # User notification about permission request result
    @staticmethod
    def send_permission_request_result_email(pr):
        if pr.approved:
            message = f"""Váš požadavek na oprávnění {pr.requested_level.name} byl schválen."""
            subject = "🎥 RS LEMMA: Požadavek na oprávnění byl schválen"
        else:
            message = f"""Váš požadavek na oprávnění {pr.requested_level.name} byl zamítnut z důvodu: {pr.response}"""
            subject = "🎥 RS LEMMA: Požadavek na oprávnění byl zamítnut"
        send_mail(
            subject,
            message,
            None,
            [pr.applicant.email],
            fail_silently=False, )

    # User notification about reservation approval request result
    @staticmethod
    def send_reservation_approval_request_result_email(reservation):
        if reservation.approved:
            message = f"""Váše rezervace na projekt {reservation.project.name} byla schválena."""
            subject = "🎥 RS LEMMA: Požadavek na rezervaci byl schválen"
        else:
            message = f"""Váše rezervace na projekt {reservation.project.name} byla zamítnuta."""
            subject = "🎥 RS LEMMA: Požadavek na rezervaci byl zamítnut"
        send_mail(
            subject,
            message,
            None,
            [reservation.applicant.email],
            fail_silently=False, )

    # Periodic admin notification about pending permission requests
    @staticmethod
    def send_pending_permissions_email():
        recipients = list(
            User.objects.filter(send_notification_on_permission_request=True).values_list('email', flat=True))
        pending_req_count = PermissionRequest.objects.filter(approved=None).count()
        if pending_req_count > 0:
            message = f"""V Rezervačním systému čeká {pending_req_count} nevyřízených žádostí o oprávnění."""
            send_mail(
                '🎥 RS LEMMA: Nevyřízené požadavky - schválení oprávnění',
                message,
                None,
                recipients,
                fail_silently=False, )

    # Periodic admin notification about pending reservation approval requests
    @staticmethod
    def send_pending_reservation_approval_email():
        recipients = list(
            User.objects.filter(send_notification_on_reservation_request=True).values_list('email', flat=True))
        pending_req_count = Reservation.objects.filter(approved=None).count()
        if pending_req_count > 0:
            message = f"""V Rezervačním systému čeká {pending_req_count} nevyřízených žádostí o schválení rezervace."""
            send_mail(
                '🎥 RS LEMMA: Nevyřízené požadavky - schválení rezervací',
                message,
                None,
                recipients,
                fail_silently=False, )

    # Periodic user notification about waiting reservation for picking up
    @staticmethod
    def send_not_picked_up_reservations_email():
        not_picked_up_reservations = Reservation.objects.filter(picked_up=False, approved=True, pickup_date_time__lt=timezone.now(),
                                                                return_date_time__gt=timezone.now()) \
            .select_related('applicant').select_related('project')
        for res in not_picked_up_reservations:
            message = f"""Vaše rezervace na projekt {res.project}
                        OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                        DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}
                        stále nebyla vyzvednuta"""
            send_mail(
                '🎥 RS LEMMA: Nevyzvednutá rezervace',
                message,
                None,
                [res.applicant.email],
                fail_silently=False, )

    # Periodic user notification about not returned reservations
    @staticmethod
    def send_not_returned_reservations_email():
        not_returned_reservations = Reservation.objects.filter(picked_up=True, resources__real_return_date__isnull=True,
                                                               return_date_time__lt=timezone.now()).distinct() \
            .select_related('applicant').select_related('project')
        for res in not_returned_reservations:
            message = f"""Vaše rezervace na projekt {res.project.name}
                        OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                        DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}
                        již skončila, ale stále nebyla vrácena. """
            send_mail(
                '🎥 RS LEMMA: Nevrácená rezervace',
                message,
                None,
                [res.applicant.email],
                fail_silently=False, )

    # User and provider notification 24hrs before picking up reservation
    @staticmethod
    def send_day_before_pick_up_email():
        planned_reservation = Reservation.objects.filter(approved=True, pickup_date_time__gt=timezone.now()) \
            .select_related('applicant').select_related('project')
        for res in planned_reservation:
            remaining_time = arrow.get(res.pickup_date_time) - arrow.get()
            if (remaining_time.seconds // 3600) == 0 and remaining_time.days == 1:
                message_for_user = f"""Vaše rezervace na projekt {res.project.name}
                            OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                            DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}
                            se blíži """
                send_mail(
                    '🎥 RS LEMMA: Blíží se termín vyzvednutí rezervace',
                    message_for_user,
                    None,
                    [res.applicant.email],
                    fail_silently=False, )
                message_for_provider = f"""Uživatel {res.applicant.fullname} si brzy přijde vyzvednout rezervaci na
                                projekt {res.project.name}
                                OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                                DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}"""
                send_mail(
                    '🎥 RS LEMMA: Blíží se termín vyzvednutí rezervace',
                    message_for_provider,
                    None,
                    [res.provider.email],
                    fail_silently=False, )

    # User and provider notification 24hrs before return reservation
    @staticmethod
    def send_day_before_return_email():
        picked_up_reservations = Reservation.objects.filter(picked_up=True, resources__real_return_date__isnull=True).distinct() \
            .select_related('applicant').select_related('project')

        for res in picked_up_reservations:
            remaining_time = arrow.get(res.return_date_time) - arrow.get()
            if (remaining_time.seconds // 3600) == 0 and remaining_time.days == 1:
                message_for_user = f"""Vaše rezervace na projekt {res.project.name}
                            OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                            DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}
                            se blíži ke konci"""
                send_mail(
                    '🎥 RS LEMMA: Blíží se termín vrácení rezervace',
                    message_for_user,
                    None,
                    [res.applicant.email],
                    fail_silently=False, )
                message_for_provider = f"""Uživatel {res.applicant.fullname} brzy přijde vrátit rezervaci vytvořenou na
                                projekt {res.project.name}
                                OD: {arrow.get(res.pickup_date_time).format('DD. MM. YYYY HH:mm')}
                                DO: {arrow.get(res.return_date_time).format('DD. MM. YYYY HH:mm')}"""
                send_mail(
                    '🎥 RS LEMMA: Blíží se termín vrácení rezervace',
                    message_for_provider,
                    None,
                    [res.provider.email],
                    fail_silently=False, )

    @staticmethod
    def send_daily_notifications():
        print('daily cron triggered')
        Mailer.send_pending_permissions_email()
        Mailer.send_pending_reservation_approval_email()
        Mailer.send_not_returned_reservations_email()
        Mailer.send_not_picked_up_reservations_email()

    @staticmethod
    def send_24h_reminders():
        print('hourly cron triggered')
        Mailer.send_day_before_pick_up_email()
        Mailer.send_day_before_return_email()
