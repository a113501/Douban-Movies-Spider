import urllib.request
import urllib
import regex as re


class Spider():

    def run(self,prefix, tag, middle, suffix):
        self.list_page = set()
        self.movie_list = set()
        self.movie_infos = []
        for i in range(0,20,20):
            url = prefix + tag + middle + str(i) +suffix
            self.list_page.add(url)
        while self.has_url(self.list_page):
            new_page = self.list_page.pop()
            page_content = self.download(new_page)
            resources = self.page_parser(page_content)
            self.url_manager(resources)
        while self.has_url(self.movie_list):
            new_movie = self.movie_list.pop()
            content = self.download(new_movie)
            info = self.content_parser(content)
            self.movie_infos.append(info)
        print(len(self.movie_infos))
        self.saver()
    def download(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
        if url is None:
            return None
        gethtml = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(gethtml)
        if response.getcode() != 200:
            return None
        return response.read().decode('utf-8')

    def has_url(self,list):
            return len(list) != 0

    def page_parser(self,cont):
        links_pattern = re.compile(r'(?<=<div class="pl2">\s\n\s+<a href=")(.*)(?="  class="">)')
        links = re.findall(links_pattern, cont)
        return links

    def url_manager(self,links):
        if links !=0:
            for i in links:
                self.movie_list.add(i)

    def content_parser(self,cont):
        infos={}
        pianming = re.compile(r'(?<=<span property="v:itemreviewed">)(.*)(?=</span>)')
        daoyan = re.compile(r'(?<=<a href="/celebrity/\d+/" rel="v:directedBy">)(.*)(?=</a>)')
        bianju = re.compile(r'<a href="/celebrity/\d+/">(.*)(?=</a></span>)')
        zhuyan = re.compile(r'(?<=<a href="/celebrity/\d+/" rel="v:starring">)(.*)(?=</a>)')
        leixing = re.compile(r'(?<=<span property="v:genre">)(.*)(?=</span>)')
        guojia = re.compile(r'(?<=制片国家/地区:</span>\s)(.*)(?=<br/>)')
        yuyan = re.compile(r'(?<=语言:</span>\s)(.*)(?=<br/>)')
        shijian = re.compile(r'(?<=<span property="v:initialReleaseDate" content=".*">)(.*)(?=</span>)')
        pianchang = re.compile(r'(?<=<span property="v:runtime" content="\d+">)(.*)(?=<br/>)')
        youming = re.compile(r'(?<=又名:</span> )(.*)(?=<br/>)')
        imdb = re.compile(r'(?<=<a href=")(.*)(?=" target="_blank" rel="nofollow">)')
        pingfen = re.compile(r'(?<=<strong class="ll rating_num" property="v:average">)(.*)(?=</strong>)')
        summary = re.compile(r'(?<=<span property="v:summary" class="">\n\s{34})(.*)(?=\s{24})')
        infos['片名'] = re.findall(pianming, cont)[0]
        infos['导演'] = re.split(r'</a> / <a href="/celebrity/\d+/" rel="v:directedBy">', re.findall(daoyan, cont)[0])
        infos['编剧'] = re.split(r'</a> / <a href="/celebrity/\d+/">', re.findall(bianju, cont)[0])
        infos['主演'] = re.split(r'</a> / <a href="/celebrity/\d+/" rel="v:starring">', re.findall(zhuyan, cont)[0])
        infos['类型'] = re.split(r'</span> / <span property="v:genre">', re.findall(leixing, cont)[0])
        infos['国家'] = re.split(r' / ', re.findall(guojia, cont)[0])
        infos['语言'] = re.split(r' / ', re.findall(yuyan, cont)[0])
        infos['上映时间'] = re.split(r'</span> / <span property="v:initialReleaseDate" content=".*">', re.findall(shijian, cont)[0])
        infos['片长'] = re.split(r'</span> / ', re.findall(pianchang, cont)[0]) ##仍有小问题，单个片长时span去不掉
        infos['又名'] =  re.split(r'/', re.findall(youming, cont)[0])
        infos['IMDB'] = re.findall(imdb, cont)[0]
        infos['评分'] = re.findall(pingfen, cont)[0]
        infos['简介'] = re.findall(summary, cont)


        return infos

    def saver(self):
        with open('spider.txt','w') as f:
            for info in self.movie_infos:
                f.write('片名:' + info['片名']+'\n')
                f.write('导演:')
                for daoyan in  info['导演']:
                    f.write(daoyan+' \ ')
                f.write('\n')
                f.write('编剧:')
                for bianju in  info['编剧']:
                    f.write(bianju+' \ ')
                f.write('\n')
                f.write('主演:')
                for zhuyan in  info['主演']:
                    f.write(zhuyan+' \ ')
                f.write('\n')

                f.write('类型:')
                for leixing in info['类型']:
                    f.write(leixing + ' \ ')
                f.write('\n')

                f.write('国家:')
                for guojia in info['国家']:
                    f.write(guojia + ' \ ')
                f.write('\n')

                f.write('语言:')
                for yuyan in info['语言']:
                    f.write(yuyan + ' \ ')
                f.write('\n')

                f.write('上映时间:')
                for shijian in info['上映时间']:
                    f.write(shijian + ' \ ')
                f.write('\n')

                f.write('片长:')
                for pianchang in info['片长']:
                    f.write(pianchang + ' \ ')
                f.write('\n')

                f.write('IMDB:' + info['IMDB'] + '\n')
                f.write('评分:' + info['评分'] + '\n')

                f.write('简介:')
                for jianjie in info['简介']:
                    f.write(jianjie)
                f.write('\n\n\n')
        f.close()


if __name__ =='__main__':
    prefix = 'https://movie.douban.com/tag/'
    tag = '2016'
    middle = '?start='
    suffix = '&type=T'
    dbmovie = Spider()
    dbmovie.run(prefix, tag, middle, suffix)

