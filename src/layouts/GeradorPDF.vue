<template>
    <div class="columns" style="padding-top: 10px; padding-left: 10px;">
        <div>
            <div v-touch-pan.prevent.stop="handler2" :style="boxTexto" class="boxTextoFora" v-show="img">
                <div v-touch-pan.prevent.stop="handler" class="noselect boxTexto" v-show="img">
                    <span v-html="getTexto"></span>
                </div>
            </div>
            
            <img id="page" :src="img" />
            
        </div>
        <div class="row items-center">
            <div class="col-3">
                <input @change="carregaFoto" id="imgInp" type="file" name="pic" accept="image/*">
            </div>
            <div class="row col-9 justify-around">
                <q-btn @click="geraPdf(true)"> Gerar PDF exemplo </q-btn>
                <q-btn @click="geraPdf(false)"> Gerar Todos os PDFs </q-btn>
            </div>
        </div>
        <div class="column q-pa-md q-mr-xl gutter-xs">
            <!-- <div class="row justify-center">
                <h5> Configurações do texto </h5>
            </div> -->
            <div v-if="mostrar" class="row items-center">
                <span class="col-auto q-mr-sm"> Posição eixo X: </span>
                <q-slider class="col" v-model="posX.value" :min="posX.min" :max="posX.max" />
                <input type="number" step="1" style="width: 70px" v-model="posX.value" />
            </div>
            <div v-if="mostrar" class="row items-center">
                <span class="col-auto q-mr-sm"> Posição eixo Y: </span>
                <q-slider class="col" v-model="posY.value" :min="posY.min" :max="posY.max" />
                <input type="number" step="1" style="width: 70px" v-model="posY.value" />
            </div>
            <div v-if="mostrar" class="row items-center">
                <span class="col-auto q-mr-sm"> Largura: </span>
                <q-slider class="col" v-model="tamX.value" :min="tamX.min" :max="tamX.max" />
                <input type="number" step="1" style="width: 70px" v-model="tamX.value" />
            </div>
            <div class="row items-center">
                <span class="col-auto q-mr-sm"> Tamanho letra: </span>
                <!-- <q-slider class="col" v-model="texto.tam.value" :min="texto.tam.min" :max="texto.tam.max" /> -->
                <input type="number" step="1" style="width: 70px" v-model="texto.tam.value" />
                <q-checkbox class="q-pl-lg" label="Justificar texto" v-model="texto.justify" />
            </div>
            <div class="row items-center">
                <span class="col-auto q-mr-sm"> Cor (hexadecimal): </span>
                <q-color-picker v-model="texto.color" />
                <!-- <q-color class="col-3 q-mr-lg" popover v-model="texto.color" /> -->
            </div>
            <div class="column gutter-xs">
                <div class="col">
                    <q-input v-model="texto.value" inverted color="tertiary" type="textarea" float-label="Texto principal"/>
                </div>
                <div class="col">
                    <q-input v-model="email.titulo" inverted color="tertiary" float-label="Titulo do email"/>
                </div>
                <div class="col">
                    <q-input v-model="email.corpo" inverted color="tertiary" type="textarea" float-label="Mensagem do email"/>
                </div>
                <div class="col">
                    <q-input v-model="nomes" inverted color="tertiary" type="textarea" float-label="Lista de pessoas"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { dom } from 'quasar';
import JSZip from 'jszip';
import JSZipUtils from 'jszip-utils';
import { saveAs } from 'file-saver';
import * as pdfMake from 'pdfmake/build/pdfmake';
import * as pdfFonts from 'pdfmake/build/vfs_fonts';
import WebFontLoader from 'webfontloader';

export default {
    name: 'GeradorPDF',
    data () {
        return {
            exe: null,
            mostrar: false,
            email: {
                titulo: '',
                corpo: '',
            },
            posX: {
                value: 50,
                max: 100,
                min: 0
            },
            posY: {
                value: 50,
                max: 100,
                min: 0
            },
            tamX: {
                value: 200,
                max: 400,
                min: 0
            },
            texto: {
                value: `Olá [NOME] você tem [IDADE] anos [EMAIL]`,
                tam: {
                    min: 1,
                    max: 1000,
                    value: 14,
                },
                color: '#FF0000',
                justify: false,
            },
            nomes: `NOME	IDADE	EMAIL
Felipe Dias	23	felipe.s.dias@outlook.com
Yasmim Cecila	24	felipe.s.dias@outlook.com`,
            img: null,
        }
    },
    created() {
        JSZipUtils.getBinaryContent("../statics/a.exe", (err, data) => {
            if(err) {
                throw err; // or handle the error
            } 

            this.exe = data;
        });

        String.prototype.replaceAll = function(search, replacement) {
            return this.replace(new RegExp(search, 'g'), replacement);
        };

        WebFontLoader.load({
            typekit: {
                id: 'cabin-sketch;adamina;advent-pro',
                api: '//use.edgefonts.net'
            } 
        });
    },
    computed: {
        boxTexto() {
            let style = `width: ${this.tamX.value}px; `;
            style += `margin-left: ${this.posX.value}px; `;
            style += `margin-top: ${this.posY.value}px; `;
            style += `font-size: ${this.texto.tam.value}pt; `;
            style += `color: ${this.texto.color}; `;
            if(this.texto.justify) {
                style += 'text-align: justify; ';
            }
            return style;
        },
        getTexto() {
            return `<strong> ${this.texto.value} </strong>`;
        }
    },
    methods: {
        handler(obj) {
            this.posX.value += obj.delta.x;
            this.posY.value += obj.delta.y;
        },
        handler2(obj) {
            this.tamX.value += obj.delta.x;
        },
        generateText(text, sub) {
            const complete = [];
            
            Object.keys(sub).forEach(key => {
                text = text.split(`[${key}]`).join(`|${sub[key]}|`);
            });

            text.split('|').forEach((item, index) => {
                if(index%2 === 0)
                    complete.push({text: item});
                else
                    complete.push({text: item, bold: true});
            });
            
            return complete;
        },
        geraPdf(justOne) {
            const zip = new JSZip();

            const headers = this.nomes.split('\n')[0].split('\t');
            let nomes = this.nomes.split('\n').filter((item, index) => (index > 0 && item.length > 2)).map(item => {
                const obj = {};
                item.split('\t').forEach((tt, index) => {
                    obj[headers[index]] = tt;
                });
                return obj;
            });

            if(justOne) nomes = [nomes[0]];

            zip.file("enviar.exe", this.exe);
            zip.file("config/titulo.txt", this.email.titulo);
            zip.file("config/mensagem.txt", this.email.corpo);
            zip.file("config/nomes.txt", nomes.map(nome => {
                return `${nome.NOME}\t${nome.EMAIL}`;
            }).join('\n'));

            const downloadZip = () => {
                zip.generateAsync({ type: 'blob' }).then(content => {
                    saveAs(content, 'Certificados.zip');
                });
            }

            nomes.forEach((nome, i) => {
                const content = [
                    {
                        text: this.generateText(this.texto.value, nome),
                        margin: [this.posX.value, this.posY.value, 5 + this.posX.max - (this.tamX.value + this.posX.value), 0],
                        fontSize: this.texto.tam.value,
                        color: this.texto.color,
                    },
                ];
    
                if(this.texto.justify)
                    content[0].alignment = 'justify';
    
                const docDefinition = {
                    pageSize: { width: this.posX.max, height: this.posY.max },
                    pageMargins: [0, 0, 0, 0],
                    background: { image: this.img },
                    content,
                }
    
                pdfMake.vfs = pdfFonts.pdfMake.vfs;

                if(justOne) {
                    pdfMake.createPdf(docDefinition).download();
                } else {
                    pdfMake.createPdf(docDefinition).getBlob(blob => {
                        console.log(blob);
                        zip.file(`pdf/${nome.NOME}.pdf`, blob);

                        if(i === nomes.length-1)
                            downloadZip();
                    });
                }
            });

        },
        carregaFoto(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                this.img = reader.result;
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.defineRanges();
                    }, 200);
                });
            };
            
        },
        defineRanges() {
            const el = document.getElementById("page");
            const maxX = dom.width(el);
            const maxY = dom.height(el);

            this.posX.max = this.tamX.max = maxX;
            this.posY.max = maxY;

            this.$nextTick(() => {
                this.posX.value = 51;
                this.posY.value = 51;
                this.tamX.value = 201;
            });

            this.$forceUpdate();
        }
    }
}
</script>

<style>

.boxTexto {
    word-wrap: break-word;
    box-shadow: 0 0 0 1px red;
    z-index: 1000;
    cursor: move;
}

.boxTextoFora {
    position: absolute;
    cursor: e-resize;
    padding-right: 5px;
}

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
}
</style>
