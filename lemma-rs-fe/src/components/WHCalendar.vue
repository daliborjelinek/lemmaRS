<template lang="pug">
  v-sheet.mt-2(rounded)
    v-calendar#wh-calendar.py-2(
      ref="calendar"
      :interval-height='30'
      :weekdays='[1,2,3,4,5]'
      first-time='07:00'
      :interval-count='22'
      interval-minutes='30'
      :interval-format="(interval) => interval.time"
      color='primary'
      type='week'
      :events="tempEvents"
      :event-ripple="false"
      @mousedown:event="startDrag"
      @mousedown:time="startTime"
      @mousemove:time="mouseMove"
      @mouseup:event="endDrag"
      @mouseleave.native="cancelDrag")
      template(v-slot:event='{ event, timed, eventSummary }')
        .v-event-draggable.noselect
          b {{ $moment(event.start).format('HH:mm')  + ' - ' + $moment(event.end).format('HH:mm')}}
        .v-event-drag-bottom(v-if='timed' @mousedown.stop='extendBottom(event)')
</template>

<script>
export default {
  name: "WHCalendar",
  data: ()=>{
    return{
      events: [],
      dragEvent: null,
      dragStartHash: null,
      createEvent: null,
      createStart: null,
      extendOriginal: null,
    }
  },
  props: ['init'],
  watch: {
    init:{
     immediate: true,
     handler(newVal,oldVal){
        this.$emit('input',newVal)
        this.events = this.restoreEvents(newVal || [])
     }
    },
    formatedEvents(newVal,oldVal){
      this.$emit('input',newVal)
      //  this.$store.commit('setCalendar',newVal)
    }
  },
  computed:{
    formatedEvents(){
      const tmp =  this.events.map(evt => {
        return {
          dow: new Date(evt.start).getDay(),
          start: this.$moment(evt.start).format('HH:mm'),
          end: this.$moment(evt.end).format('HH:mm'),
        }
      })
      return tmp
    },
    tempEvents(){
      return [...this.events]
    },

  },
  methods: {
    restoreEvents(formatedEvents){
      const tmp =  formatedEvents.map(evt =>{
        const curDay = this.$moment().startOf('week').add(evt.dow,'days')
        return {
          start: this.$moment(curDay.format('YYYY-MM-DD') + ' ' +  evt.start,'YYYY-MM-DD HH:mm').valueOf(),
          end: this.$moment(curDay.format('YYYY-MM-DD') + ' ' +  evt.end,'YYYY-MM-DD HH:mm').valueOf(),
          startTimeStr: evt.start,
          endTimeStr: evt.end,
          color: 'primary',
          timed: true,
          name: '⌛'
        }
      })
      return tmp
    },
    startDrag ({ event, timed }) {
      if (event && timed) {
        this.dragStartHash = event.start + event.end
        this.dragEvent = event
        this.dragTime = null
        this.extendOriginal = null
      }
    },
    startTime (tms) {

      const mouse = this.toTime(tms)

      if (this.dragEvent && this.dragTime === null) {
        const start = this.dragEvent.start

        this.dragTime = mouse - start
      } else {
        this.createStart = this.roundTime(mouse)
        this.createEvent = {
          name: `⌛`,
          color: 'primary',
          start: this.roundTime(mouse),
          end: this.roundTime(mouse,false),
          timed: true,
        }
        this.events.push(this.createEvent)
      }
    },
    extendBottom (event) {
      this.createEvent = event
      this.createStart = event.start
      this.extendOriginal = event.end
    },
    mouseMove (tms) {
      const mouse = this.toTime(tms)

      if (this.dragEvent && this.dragTime !== null) {
        const start = this.dragEvent.start
        const end = this.dragEvent.end
        const duration = end - start
        const newStartTime = mouse - this.dragTime
        const newStart = this.roundTime(newStartTime)
        const newEnd = newStart + duration

        this.dragEvent.start = newStart
        this.dragEvent.end = newEnd
      } else if (this.createEvent && this.createStart !== null) {
        const mouseRounded = this.roundTime(mouse, false)
        const min = Math.min(mouseRounded, this.createStart)
        const max = Math.max(mouseRounded, this.createStart)

        this.createEvent.start = min
        this.createEvent.end = max
        if(new Date(min).getDay() !== new Date(max).getDay()) this.cancelDrag()

      }
    },
    endDrag (clickedEvent) {
      if(this.dragStartHash === this.dragEvent?.start + this.dragEvent?.end) this.events = this.events.filter(e => e.start !== clickedEvent.event.start)
      this.dragTime = null
      this.dragEvent = null
      this.createEvent = null
      this.createStart = null
      this.extendOriginal = null
    },
    cancelDrag () {
      if (this.createEvent) {
        if (this.extendOriginal) {
          this.createEvent.end = this.extendOriginal
        } else {
          const i = this.events.indexOf(this.createEvent)
          if (i !== -1) {
            this.events.splice(i, 1)
          }
        }
      }

      this.createEvent = null
      this.createStart = null
      this.dragTime = null
      this.dragEvent = null
    },
    roundTime (time, down = true) {
      const roundTo = 30 // minutes
      const roundDownTime = roundTo * 60 * 1000

      return down
          ? time - time % roundDownTime
          : time + (roundDownTime - (time % roundDownTime))


    },
    toTime (tms) {

      return new Date(tms.year, tms.month - 1, tms.day, tms.hour, tms.minute).getTime()
    },
  },
}
</script>

<style scoped lang="scss">
.v-event-draggable {
  padding-left: 6px;
}

.v-event-timed {
  user-select: none;
  -webkit-user-select: none;
}

.v-event-drag-bottom {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4px;
  height: 4px;
  cursor: ns-resize;

  &::after {
    display: none;
    position: absolute;
    left: 50%;
    height: 4px;
    border-top: 1px solid white;
    border-bottom: 1px solid white;
    width: 16px;
    margin-left: -8px;
    opacity: 0.8;
    content: '';
  }

  &:hover::after {
    display: block;
  }
}
</style>
