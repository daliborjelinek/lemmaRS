<template>
  <div>
    <div ref="html" class="d-none" style="font-size:8px; font-family: arial; width:386px; position: relative;">
      <p style="text-align: center"><b>Smlouva o výpůjčce majetku FI</b></p><br/>
      <p style="text-align: center">podle ustanovení § 2193 a násl. zákona č. 89/2012 Sb., občanský zákoník</p><br/>
      <p>
        <b>Vypůjčitel</b>: {{ name }} učo: {{ uco }} bytem:
        {{ address }} a Masarykova univerzita,
        Fakulta informatiky,
        Botanická 68a, 602 00 Brno, (dále jen „<b>půjčitel</b>“) zastoupená doc. RNDr. Petrem Sojkou, vedoucím
        Laboratoře
        elektronických a multimediálních aplikací, uzavírají následující smlouvu o výpůjčce inventáře fakulty.<br/>
        <b>Vypůjčitel</b> svým podpisem potvrzuje, že mu byly dne {{ $moment().format('DD. MM. YYYY HH:mm') }} níže
        uvedenou pověřenou osobou zapůjčeny do <b>{{ returnDate }}</b> tyto předměty:
      </p>
      <div :style="'position:absolute; top: '+offset+'px; text-align: justify'">
        <ol style="margin-left: 10px;">
          <li>
            Obě smluvní strany potvrzují, že si předmět výpůjčky před jeho předáním vypůjčiteli k užívání pečlivě
            prohlédly
            konstatují, že na něm nejsou žádné nedostatky, které by bránily jeho řádnému užívání.
          </li>

          <li style="margin: 10px 0;">Vypůjčitel je oprávněn užívat zapůjčené předměty řádně a v souladu s účelem, ke
            kterému obvykle slouží, je povinen
            chránit je před poškozením, ztrátou nebo zničením a nesmí je přenechat k užívání jinému.
          <li style="margin: 10px 0;">Vypůjčitel odpovídá za ztrátu zapůjčených předmětů a v případě jejich ztráty se
            zavazuje nahradit fakultě jejich hodnotu
            v plné výši, pokud neprokáže, že ke ztrátě došlo zcela nebo zčásti bez jeho zavinění (pro tento případ
            půjčitel doporučuje
            sjednat pojištění odpovědnosti za škodu).
          </li>

          <li style="margin: 10px 0;">Vypůjčitel se zavazuje bezodkladně oznámit ztrátu, poškození nebo jiné závady
            svěřených předmětů bezprostředně na
            e-mailovou adresu lemma-adm@fi.muni.cz nebo tajemnik@fi.muni.cz
          </li>

          <li style="margin: 10px 0;">Vypůjčitel je povinen zapůjčené předměty vrátit v termínu {{ returnDate }},
            respektive kdykoliv na výzvu fakulty.
          </li>

          <li style="margin: 10px 0;">Ve výjimečném případě je vypůjčitel oprávněn předat předmět výpůjčky přímo dalšímu
            uživateli, ovšem pouze za
            předpokladu, že nový uživatel písemně potvrdí vypůjčiteli převzetí předmětu výpůjčky bez jakýchkoli
            nedostatků. Toto
            písemné potvrzení je vypůjčitel povinen předat následující pracovní den pověřené osobě zajišťující
            zapůjčování vybavení
            laboratoře. V případě, že vypůjčitel umožní užívání věci třetí osobou bez písemného potvrzení předmětu
            výpůjčky anebo
            tato osoba nebyla uživatelem laboratoře LEMMA, je povinen nahradit případnou vzniklou škodu.
          </li>

          <li style="margin: 10px 0;">Nebude-li věc vrácena vypůjčitelem půjčiteli řádně a včas, je vypůjčitel povinen
            uhradit půjčiteli smluvní pokutu ve
            výši jednoho promile {{ totalCost / 1000 | currency }} z pořizovací ceny za každou nevrácenou věc a za
            každý, i započatý den
            prodlení s plněním této povinnosti. Uplatněním nároku na smluvní pokutu není dotčen nárok na náhradu škody.
          </li>
        </ol>

        <div style=" float: left; margin-left: 50px; margin-top: 50px">.................................<br><br>Vypůjčitel
        </div>
        <div style="float: right; margin-right: 50px; margin-top: 50px">.................................<br><br>Pověřená
          osoba
        </div>
      </div>
    </div>
    <iframe class="d-none" :src="pdf"
            style="width: 100%; height: 1200px; margin: 0; padding: 0;"></iframe>
  </div>

</template>

<script>
import jsPDF from 'jspdf'

import {robotoNormal} from '@/assets/jsPDF/roboto-normal'
import {robotoBold} from '@/assets/jsPDF/roboto-bold'

import 'jspdf-autotable'

export default {
  props: ['reservation'],
  name: "PdfCreator",
  data() {
    return {
      pdf: null,
      doc: null,
    }
  },
  created() {
  },
  computed: {
    offset() {
      // 80 - html starts on y = 80 (70 because we want 10px margin)
      // 632 * 446 = A4 dimensions in pixels
      // 60 = margin on every page

      return this.doc?.lastAutoTable ? ((632 - 60) * (this.doc.lastAutoTable.pageCount - 1)) + (this.doc.lastAutoTable.finalY - 70) : 0
    },
    resources() {
      if (this.reservation.resources) {
        return this.reservation.resources.map((res) => {

          return [res.inv_numbers.join('; '), res.resource_str, this.$options.filters.currency(res.cost), this.$options.filters.currency(res.cost / 1000)]
        })
      } else return []
    },
    totalCost() {
      return this.reservation?.resources.reduce((partial_sum, res) => partial_sum + res.cost, 0)
    },
    name() {
      return this.reservation?.applicant?.fullname
    },
    uco() {
      return this.reservation?.applicant?.username
    },
    address() {
      return this.reservation?.applicant?.address
    },
    returnDate() {
      return this.$moment(this.reservation?.return_date_time).format('DD. MM. YYYY HH:mm')
    }
  },
  methods: {
    addHtml(doc) {
      doc.html(this.$refs.html, {x: 0, y: 50, callback: this.save, autoPaging: 'text', margin: [30, 30, 30, 30]})
    },
    save(doc) {
      this.pdf = doc.output('datauristring')
      doc.autoPrint();
      doc.output('dataurlnewwindow');
    },
    async print() {
      this.doc = new jsPDF("p", "px", "a4");
      this.doc.addFileToVFS('arial-normal.ttf', robotoNormal);
      this.doc.addFileToVFS('arial-bold.ttf', robotoBold);
      this.doc.addFont('arial-normal.ttf', 'arial', 'normal');
      this.doc.addFont('arial-bold.ttf', 'arial', 'bold');
      this.doc.addImage('https://sablony.muni.cz/media/3131667/inf-lg-cze-rgb.jpg', 'JPEG', 20, 20, 70, 50)
      this.doc.autoTable({
        startY: 200,
        startX: 20,
        head: [['Inventární číslo', 'Název', 'Cena', 'Promile']],
        rowPageBreak: 'auto',
        styles: {font: 'arial'},
        columnStyles: {2: {cellWidth: 50, halign: 'right'}, 3: {cellWidth: 50, halign: 'right'}},
        body: this.resources
      })
      this.addHtml(this.doc)
    }

  }
}
</script>

