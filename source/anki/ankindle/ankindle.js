//正面

<div id="front" class="section" onclick="playAudio('stem')">
<div class="items">
<a onclick="event.stopPropagation();" href="eudic://x-callback-url/searchword?word={{text:stem}}&x-success=anki://">
<span id="stem">{{stem}}</span></a>
<span id="audio"></span>
</div>
</div>

{{#usage}}
<div class="section">
<div id="front-extra1" class="items">{{usage}}</div>
</div>

<div class="section">
<div id="front-extra2" class="items">{{title}} ({{authors}})</div>
</div>
{{/usage}}

<audio id="player" src=""></audio>


//通用

</style>

<style>
/*
ODH Template
author:ninja huang
site:https://github.com/ninja33/odh
*/

.card {
  margin: 12px;
  font-size: 16px;
  text-align: left;
  background-color: #fff;
  font-family:"Segoe UI", Arial, "Microsoft Yahei", sans-serif;
}

.section {
  color: #333;
  background-color: #f5f5f5;
}

.items{
  padding:10px;;
  background-color: #f5f5f5;
}
.section a{
  color: #333;
  text-decoration:none;
}

#audio{
  margin-left: 5px;
}

#audio img{
  width: 64px;
  height: 64px;
}

#front, 
#back{
  line-height: 1.4em;
}

#front{
  font-size: 2em;
  font-weight: 300;
  color:#444;
  border-bottom: 3px solid #666;
}

#front-extra1{
 
}

#front-extra2{
  font-size: 0.8em;
  text-align:right;
  font-style:Segoe UI;
  border-top: 1px solid #ddd;
}

#back{
  background-color:white;
}

#back-extra1{
}
#back-extra1{
}

.odh-playsound {
  vertical-align: text-bottom;
  margin: 0 3px;
}

.chn_tran{
  /* change to 'display:none;' if you want to hide Chinese */
  display:initial; 
}

.chn_sent{
  /* change to 'display:none;' if you want to hide Chinese */
  display:initial; 
}


/*删除下方样式，显示中文释义*/
.explanation_box .text_blue{
  display:none;
}
/*删除下方样式，显示中文例句*/
.explanation_item ul li p+p{
  display:none;
}
/*删除下方样式，显示全部例句(若有)，目前仅显示第一句*/
.explanation_item ul li+li{
  display:none;
}

.vExplain_r ul li+li{
  display:none;
}

.vExplain_r ul li p+p{
  display:none;
}


.explanation_label>.hightlight{
  font-style:italic;
  font-size         : 1em;
  border-radius     : 5px; 
  color             : white; 
  padding           : 1px 4px;
  margin-right      : 5px;
  text-decoration   : none;
  text-align        : center;
}
</style>

<script>
function playAudio(wordID) {
    var word = document.getElementById(wordID).innerText;
    var base = "http://dict.youdao.com/dictvoice?audio="; 
    //var base = "http://fanyi.baidu.com/gettts?lan=en&text=";
    var audioSrc = base + encodeURI(word);
    //检查是否为电脑端
    if(typeof(py)=="object"){
    //如果是电脑端，需安装插件 #498789867(replay button on card)才能发音
        py.link("ankiplay"+audioSrc)
    }else{
        var player=document.getElementById('player')
        player.src=audioSrc
        player.play()
    }
}

function fixPosition(section){
    [].forEach.call(document.querySelectorAll(section), function(div) {
        div.innerHTML = div.innerHTML.replace(/.?\[(.+?)[\s|-].+/g,"$1").toLowerCase();
    });
}
//帮助函数:词性高亮
function highlightTag(section){
    var colorMap = {
        'n':'#e3412f',
        'a':'#f8b002',
        'adj':'#f8b002',
        'ad':'#684b9d',
        'adv':'#684b9d',
        'v':'#539007',
        'vi':'#539007',
        'vt':'#539007',
        'verb':'#539007',
        'phrasal':'#04B7C9',
        'phrase':'#04B7C9',
        'phr':'#04B7C9',
        'prep':'#04B7C9',
        'conj':'#04B7C9',
        'pron':'#04B7C9',
        'art':'#04B7C9',
        'num':'#04B7C9',
        'int':'#04B7C9',
        'interj':'#04B7C9',
        'modal':'#04B7C9',
        'aux':'#04B7C9',
        'pl':'#D111D3',
        'abbr':'#D111D3',
        'idiom':'#D111D3',
        'Fig':'#D111D3',
        'fig':'#D111D3',
        'quant':'#D111D3'
    };
    [].forEach.call(document.querySelectorAll(section), function(div) {
        div.innerHTML = div.innerHTML.replace(/\b[a-z]+/g, function(symbol) {
            if (colorMap[symbol]) {
                return '<a class="hightlight" style="background-color:' 
                             + colorMap[symbol] + ';" >'+ symbol + '</a>';
            } else {
                return symbol;
            }
        });
    });
}
</script>
<style>



//背面

<div id="front" class="section">
<div class="items">
<span id="stem">{{stem}}</span></a>
<span id="audio"></span>
</div>
</div>

{{#usage}}
<div class="section">
<div id="front-extra1" class="items">{{usage}}</div>
</div>

<div class="section">
<div id="front-extra1" class="items"></div>
</div>
{{/usage}}






<div id="back" class="section">
{{mdx_dict}}
</div>

<script>
fixPosition(".explanation_label");
highlightTag(".explanation_label");
</script>