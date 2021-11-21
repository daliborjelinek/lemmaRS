<template>
  <div>
    <div ref="html" class="d-none" style="font-size:11px; font-family: arial; width:535px;">
      <p style="text-align: center"><b>Smlouva o výpůjčce majetku FI</b></p><br/>
      <p style="text-align: center">podle ustanovení § 2193 a násl. zákona č. 89/2012 Sb., občanský zákoník</p><br/>
      <p>
        <b>Vypůjčitel</b>: {{ name }} <b>učo</b>: {{ uco }} bytem:
        {{ address }} a Masarykova univerzita,
        Fakulta informatiky,
        Botanická 68a, 602 00 Brno, (dále jen „<b>půjčitel</b>“) zastoupená doc. RNDr. Petrem Sojkou, vedoucím
        Laboratoře
        elektronických a multimediálních aplikací, uzavírají následující smlouvu o výpůjčce inventáře fakulty.<br/>
        <b>Vypůjčitel</b> svým podpisem potvrzuje, že mu byly dne 15. 11. 2021 08:00 níže uvedenou pověřenou osobou
        zapůjčeny do
        <b>{{ returnDate }}</b> tyto předměty:
      </p>
    </div>
    <div ref="html2" class="d-none" style="font-size:11px; font-family: arial; width:480px;">
      <ol style="text-align: justify">
        <li style="margin: 10px 0;">
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

        <li style="margin: 10px 0;">Vypůjčitel je povinen zapůjčené předměty vrátit v termínu 16. 11. 2021 08:00,
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
          výši jednoho promile (30 Kč) z pořizovací ceny za každou nevrácenou věc a za každý, i započatý
        </li>
      </ol>

      <div style=" float: left; margin-left: 50px; margin-top: 50px">.................................<br><br>Vypůjčitel
      </div>
      <div style="float: right; margin-right: 50px; margin-top: 50px">.................................<br><br>Pověřená
        osoba
      </div>
    </div>
    <iframe class="d-none" :src="pdf"
            style="width: 100%; height: 1200px; margin: 0; padding: 0;"></iframe>
  </div>

</template>

<script>
import jsPDF from 'jspdf'
import {arial} from '@/assets/jsPDF/arial-normal'
import {arialBold} from '@/assets/jsPDF/arial-bold'
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
    resources() {
      if (this.reservation.resources) {
        return this.reservation.resources.map((res) => {

          return [res.inv_numbers.join('; '), res.resource_str, this.$options.filters.currency(res.cost), this.$options.filters.currency(res.cost / 1000) ]
        })
      } else return []
    },
    name(){
      return this.reservation?.applicant?.fullname
    },
    uco(){
      return this.reservation?.applicant?.username
    },
    address(){
      return this.reservation?.applicant?.address
    },
    returnDate(){
      return this.reservation?.return_date_time
    }
  },
  methods: {
    addHtmlStart(doc) {
      console.log(doc.lastAutoTable)
      doc.html(this.$refs.html, {x: 0, y: 50, callback: this.save, autoPaging: 'text', margin: [30, 30, 30, 40]})
    },
    addHtmlEnd(doc) {
      console.log(doc.lastAutoTable)
      doc.html(this.$refs.html2, {
        x: 30,
        y: ((842 - 60) * (doc.lastAutoTable.pageCount - 1)) + doc.lastAutoTable.finalY,
        callback: this.save,
        autoPaging: 'text',
        margin: [30, 30, 30, 40]
      })
    },
    save(doc) {
      console.log(doc)
      this.pdf = doc.output('datauristring')
      doc.autoPrint();
      doc.output('dataurlnewwindow');

    },
    print() {
      this.doc = new jsPDF("p", "pt", "a4");
      this.doc.addFileToVFS('arial-normal.ttf', arial);
      this.doc.addFileToVFS('arial-bold.ttf', arialBold);
      this.doc.addFont('arial-normal.ttf', 'arial', 'normal');
      this.doc.addFont('arial-bold.ttf', 'arial', 'bold');
      this.doc.setFont("arial");
      this.doc.addImage('https://sablony.muni.cz/media/3131667/inf-lg-cze-rgb.jpg', 'JPEG', 20, 20, 70, 50)
      this.doc.autoTable({
        startY: 220,
        startX: 20,
        head: [['Inventární číslo', 'Název', 'cena', 'Promile']],
        rowPageBreak: 'auto',
        styles: {font: 'arial'},
        columnStyles: {text: {cellWidth: 'auto'}},
        body: this.resources
      })
      this.addHtmlStart(this.doc)
      //this.addHtmlEnd(this.doc)
    }

  }
}
</script>

