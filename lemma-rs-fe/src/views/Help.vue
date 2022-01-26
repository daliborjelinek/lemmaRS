<template lang="pug">
  v-dialog(v-model="helpDialog" scrollable max-width="900px")
    v-card()
      v-toolbar(color="primary", dark)
        | Rezervační systém
        v-spacer
        v-btn(icon, @click="helpDialog = false")
          v-icon mdi-close
      v-card-text.pa-0
        v-container(style="height:calc(100% - 48px)")
          v-tabs(v-model="tab" background-color="#272727")
            v-tab Nápověda
            v-tab FAQ
            v-tab Hlášení chyb
          v-tabs-items.inner-scroll(v-model="tab")
            v-tab-item.mt-4.help
              .display-4.mb-0
                i Milý uživateli,

              | vítej v rezervačním systému laboratoře LEMMA. V této aplikaci si můžeš zarezervovat audiovizuální techniku pro tvorbu vlastních projektů. Před první rezervací si prosím pečlivě přečti tuto nápovědu.

              h2.py-5 🚩 Před Tvou první rezervací…
              h3.pb-4  🔐 Oprávnění k rezervaci
              p K tomu, abys rezervace mohl vytvářet, potřebuješ získat oprávnění, které schvaluje administrátor laboratoře. Oprávnění mají dvě úrovně:
              ul
                li
                  b Lemma&nbsp;
                  span – o toto oprávnění si mohou zažádat všichni studenti, kteří mají zapsaný některý z předmětů laboratoře. Umožňuje rezervaci většiny zdrojů.
                li
                  b Lemma nad 100&nbsp;
                  span – jedná se o oprávnění k rezervování nákladné techniky, k jehož udělení je podmínkou uzavření
                  span.font-weight-bold &nbsp;pojištění odpovědnosti&nbsp;
                  span u libovolné pojišťovny a předání potvrzení o tomto pojištění paní Lysákové. Po předání potvrzení můžeš zaslat žádost o tuto úroveň oprávnění.
              p Oprávnění se zpravidla uděluje na rok. Po expiraci je nutné o oprávnění zažádat znovu.
              p
                span O oprávnění můžeš zažádat na stránce
                v-btn.mx-1(@click="$router.push({name: 'Permissions'})" color="primary" x-small) Oprávnění
                span .
              p
                span Pokud se chceš podívat jaká opravní jsou pro konkrétní zdroje potřeba, zobraz si zdroje jako list kliknutím na ikonu
                v-btn.mx-1(x-small)
                  v-icon(small) mdi-format-list-bulleted
                span v pravém panelu.
              h3.pb-5 ✨ Vytvoření projektu
              p Každá rezervace musí být přiřazena k existujícímu projektu. Projekt můžeš vytvořit buď Ty, nebo kdokoliv z Tvých kolegů, pokud pracujete v týmu. Pří vytváření projektů můžeš označit kolegy, kteří mohou na daný projekt rezervovat zdroje. Díky tomu se jim projekt zobrazí v našeptávači při vytváření rezervace, čímž jim ušetříš práci s vytvářením projektu a všechny rezervace budou pohromadě.
              p
                span Projekt můžeš vytvořit na stránce
                v-btn.mx-1(@click="$router.push({name: 'Projects'})" color="primary" x-small) Projekty
                span , nebo v levém panelu při vytváření samotné rezervace kliknutím na tlačítko
                v-btn.mx-1(x-small fab)
                  v-icon(small) mdi-plus-circle
                span v našeptávači existujících projektů.

              p Vyvaruj se prosím vytváření duplicitních projektů pro jedno dílo.
              p Po dokončení práce na projektu označ projekt jako dokončený, aby bylo jasné že už se ani Ty ani Tví kolegové nechystáte vytvářet k tomuto projektu další rezervace.
              h2.pb-5 🛒 Rezervace
              p Pokud máš schválené oprávnění alespoň na základní úroveň a máš vytvořený projekt, nic Ti nebrání ve vytvoření rezervace. Ačkoliv můžeš začít rovnou vybírat zdroje, je dobré znát několik pravidel, kterými se systém řídí, abys jeho možnosti využil naplno.
              ul
                li  Zdroje má ve správě několik výdejářů, kteří jsou na různých místech a mají odlišnou pracovní dobu. Proto jedna rezervace může být složena pouze ze zdrojů od jednoho výdejáře. Pokud potřebuješ zdroje od různých výdejářů, musíš vytvořit víc rezervací.
                li  Systém ti umožní nastavit datum vyzvednutí a vrácení zdrojů pouze v pracovní době výdejáře.

              p Z těchto důvodů je lepší při vytváření rezervace volit následující postup:

              ol
                li
                  span V levém panelu vyber výdejáře (naprostou většinu má na starosti paní Lysáková. Pokud se chceš podívat, jaká technika patří kterému výdejáři, zobraz si zdroje jako seznam kliknutním na ikonnu
                  v-btn.mx-1(x-small)
                    v-icon(small) mdi-format-list-bulleted
                  span )
                li Vyber od kdy do kdy chceš zdroje rezervovat.
                li Vyber (nebo vytvoř) projekt, na který chceš zdroje rezervovat.

              p Po zvolení požadovaných hodnot se ti automaticky vyfiltrují zdroje, které je možné v daný termín rezervovat. Pomocí filtrů v pravém panelu můžeš zvolit, zda chceš zdroje, které z nějakého důvodu nelze rezervovat, úplně skrýt, nebo zobrazit s výstražnou ikonkou a deaktivovaným tlačítkem pro rezervaci.

              p Pak už jen stačí vybrat zdroje a kliknout na tlačítko odeslat.
              p
                span Určitě koukni také záložku
                v-btn.mx-1(x-small color="primary" @click="tab = 1") FAQ

              .display-4
               i Hodně štěstí s Tvými projekty!


            v-tab-item.mt-4.help
              h2.pb-4 Proč nemůžu zdroje rezerovovat?
              p Existuje několik důvodů proč není možné kliknout na tlačítko rezervovat. Každý z důvodů je symbolizovaný konkretní ikonou v červeném poli.
              table
                tr
                  td
                    v-chip(class="ma-2" label color="#4c0000c2" title="nemáte dostatečné oprávnění")
                      v-icon() mdi-shield-lock
                  td Pro rezervování zdroje nemáte dostatečné oprávnění.
                tr
                  td
                    v-chip(class="ma-2" label color="#4c0000c2" title="Zdroj není k dispozici")
                      v-icon() mdi-heart-broken
                  td Zdroj nelze rezerovvat, jelikož je vyřazený, nebo v opravě.
                tr
                  td
                    v-chip(class="ma-2" label color="#4c0000c2" title="Zdroj je již v daném termínu rezervován")
                      v-icon() mdi-clock-alert
                  td Ve vybraném termínu je tento zdroj již rezervován někým jiným. Po kliknutí na tlačítko kalendář si můžete zobrazit, detaily o dalších rezervacích daného zdroje a případně svou rezervaci přeplánovat.
                tr
                  td
                    v-chip(class="ma-2" label color="#4c0000c2" title="Pro rezervování tohoto zdroje je potřeba vybrat jiného výdejáře")
                      v-icon() mdi-account-cog
                  td Jedna rezervace může obsahovat zdroje pouze od jednoho výdejáře. Pro rezervování takového zdorje buď vyberte příslušného výdajáře, nebo vytvořte samostatnou rezervaci.
                tr
                  td
                    v-chip(class="ma-2" label color="#fb8c00c2" title="Zdroj nebyl vrácen")
                      v-icon() mdi-selection-ellipse
                  td Takto označený zdroj je možné rezervovat, ale je možné, že při vyzvednutí nebude k dispozici, protože předchozí rezevace tohoto zdroje již skončila, ale navzdory tomu zdroj stále nebyl vrácen.
            v-tab-item.mt-4.help
              h2.py-4 Narazili jste na chybu, nebo máte návrh na zlepšení systému?
              p Popis ideálně včetně snímků obrazovky zašlete na email&nbsp;
                a(href="mailto:git+lemma-lemmars-16040-issue-@gitlab.fi.muni.cz") git+lemma-lemmars-16040-issue-@gitlab.fi.muni.cz


</template>
<script>

export default {
  name: 'help',
  data: () => ({
    helpDialog: false,
    tab: 0
  }),
  computed: {},
  methods: {
    show() {
      this.helpDialog = true
    },
  },
};
</script>

<style type="scss">
.help {
  font-size: 17px !important;
  line-height: initial;
  text-align: justify;
}

.help .display-4 {
  font-size: 2rem !important;
}

.help li {
  margin: 10px 0;
}

.inner-scroll {
  height: 100%;
  overflow-y: auto;
}

.help ol, .help ul {
  padding-left: 3rem;
}

.help table tr {
  vertical-align: middle;
}

</style>
