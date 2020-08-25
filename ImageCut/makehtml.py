from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
# hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}


allCont = ''    #가장 마지막 html
allThumb = ''  #써머리
outBody = ''

def wrapStringInHTMLWindows(outBody):
    from webbrowser import open_new_tab

    filename = 'program' + '.html'
    f = open(filename,'wb')
    f.write(outBody.encode())
    f.close()
    open_new_tab(filename)


def goList(getUrl , thumbCnt) :
    global outBody
    req = Request( getUrl)
    res = urlopen(req)
    # html = res.read().decode('utf-8')

    bs = BeautifulSoup(res.read(), 'html.parser')
    title = str(bs.find('title')).replace(' - RYMD','')
    title = title.replace('<title>','').replace('</title>', '')

    if thumbCnt < 10:
        thumbCnt = '0' + str(thumbCnt)

    tags = bs.findAll('div', attrs={'class': 'cont'})
    getThumb = bs.find('img', attrs={'class': 'BigImage'})
    getThumbUrl = str(getThumb['src']).replace('//','<img width="400" height="400" class="thumb-img" src="http://') + '">'


    cont = str(tags[1]).replace('<div class="cont">','')
    cont = cont.replace('</center> </div>','</center>')
    cont = cont.replace('<img ec-data-src="//eyemarket.diskn.com/SCRIPT/TOP-LOGO.jpg"/><br/><br/><br/>','')
    cont = cont.replace('ec-data-src="', 'src="http:')

    allThumb = '<table width="400"><tr><td>' +            str(getThumbUrl)           +           '</td></tr><tr><td class="t_number" align="center">' + str(thumbCnt)  +'</td></tr><tr><td align="center" class="t_title"  >' + str(title)  +  '</td></tr></table>'
    outBody += allThumb

    insertNumber = "<div class='t_number' style='font-size:72px; font-weight:900; color:#666;  text-align:center;'>" + str(thumbCnt) + "</div>"
    global allCont
    allCont = allCont+ insertNumber + cont

getPro = [
'http://rymds.com/product/detail.html?product_no=11&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=354&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=351&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=353&cate_no=1&display_group=4',
'http://rymds.com/product/detail.html?product_no=11&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=354&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=351&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=353&cate_no=1&display_group=4',
'http://rymds.com/product/detail.html?product_no=11&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=354&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=351&cate_no=1&display_group=2',
    'http://rymds.com/product/detail.html?product_no=353&cate_no=1&display_group=4',
]

thumbCnt = 0

#써머리 출력
outBody =  "<html><head><style>@import url('https://fonts.googleapis.com/css2?family=Overpass:wght@900&display=swap');             @font-face {     font-family: 'S-CoreDream-3Light';     src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');     font-weight: normal;     font-style: normal;}             .t_number { font-family: 'Saira Stencil One', cursive; font-family: 'Overpass', cursive; font-weight:900; font-size:48px;	color:#666;  text-align:center; } td .t_title { font-family: 'S-CoreDream-3Light'; font-size: 24px; height : 80px;  vertical-align:top;} .thumb-img { border-radius: 4%;}   td { text-align:center; } </style></head><body><table align='center'><tr><td colspan='2'> "


def start() :
    global outBody, thumbCnt, allCont
    for i in getPro :
        thumbCnt += 1
        goList(  i , thumbCnt )
        if ( thumbCnt % 2 == 0 ) :
            outBody += "</td></tr><tr><td colspan='2'>"
        else : outBody += "</td><td>"

    outBody += ("</td></tr></table>")

    outBody += ("--------------------------------------------------------------------------------")
    outBody +=("--------------------------------------------------------------------------------")
    outBody +=("--------------------------------------------------------------------------------")
    outBody += ("")
    outBody +=("")

    allCont = allCont.replace('src="http://eyemarket.diskn.com/SCRIPT/PAGE-BOTTOM.jpg"/>','/>')
    allCont = allCont.replace('src="http://eyemarket.diskn.com/SCRIPT/notice.jpg"/>','/>')
    allCont = allCont.replace('http://eyemarket.diskn.com/A_F/2019/siver-daller-eucal-tree/(9).jpg','')
    allCont = allCont.replace('http://eyemarket.diskn.com/SCRIPT/TOP-LOGO.jpg','')

    allCont = allCont.replace('<img />', '')
    allCont = allCont.replace('</img>', '')
    allCont = allCont.replace('<br/><br/><br/><br/><br/><br/>', '')

    #상세 출력
    outBody +=  allCont
    outBody += ("")
    outBody += ("")
    outBody += ("--------------------------------------------------------------------------------")
    outBody += ("--------------------------------------------------------------------------------")
    outBody += ("--------------------------------------------------------------------------------")

    outBody += "</body></html>"

    wrapStringInHTMLWindows(outBody)
