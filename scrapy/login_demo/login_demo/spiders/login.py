from scrapy.http import Request,FormRequest
import scrapy



class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com"]
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}

    # 编写start_requests()方法，第一次会默认调取该方法中的请求
    def start_requests(self):
        # 首先爬一次登录页，然后进入回调函数 parse()
        # https://github.com/login
        return [Request("https://github.com/session", meta={"cookiejar": 1}, callback=self.parse)]
    def parse(self, response):
        # 设置要传递的post信息，此时没有验证码字段
        # https://github.com/session
        '''
        密码自寻
        commit=Sign+in&authenticity_token=QSgzMRSU3q5roSz%2FVc32TjwLC4V27xkno00UszU6iE%2F21Cv8F1m25Pa0l5QSGqvRarpm715fEv4J1aumC0QlgQ%3D%3D
        &add_account=
        &login=Monkey-D-Jie
        &password=密码自寻
        &webauthn-conditional=undefined
        &javascript-support=true
        &webauthn-support=supported
        &webauthn-iuvpaa-support=supported
        &return_to=https%3A%2F%2Fgithub.com%2Flogin&allow_signup=
        &client_id=&integration=
        &required_field_770c=
        &timestamp=1756364214153&timestamp_secret=7bc9e51cba78fa7915858f9a741c032a97b35fdf060e2b1810c52a944cf03ad0
        '''
        data ={
            "login":"Monkey-D-Jie",
            "password":"密码自寻"
        }
        print("尝试登录中。。。。。。。。")
        #  通过FormRequest.from_response()进行登录
        return [FormRequest.from_response(response,
                                          # 设置cookie
                                          meta={"cookiejar":response.meta["cookiejar"]},
                                          # 设置header，模拟浏览器请求
                                          headers = self.header,
                                          # 设置post表单中的数据
                                          formdata= data,
                                          # 设置回调函数，指明爬取到数据后，下一步怎么处理。
                                          callback = self.next
                                          )]
    def next(self,response):
        # 将获取到的页面输出保存到本地的html文件中，下同
        data = response.body
        # 当前项目所在的绝对路径下
        fh = open("H:/myIdeaWorkSpace/PythonStudy/scrapy/login_demo/next.html","wb")
        fh.write(data)
        fh.close()
        titles = response.xpath("/html/head/title/text()").extract()
        print("next------->>>>>>" + ", ".join(titles))
        # 此处类似的，登录成功后，将会跳转到对应的页面去，这里我们用的账户登录的主页。
        yield Request("https://github.com/Monkey-D-Jie",meta={"cookiejar":True},callback=self.next2)
    def next2(self,response):
        data = response.body
        fh = open("H:/myIdeaWorkSpace/PythonStudy/scrapy/login_demo/next2.html", "wb")
        fh.write(data)
        fh.close()
        # 在该方法中，将response的相关信息打印出来
        titles2 = response.xpath("/html/head/title/text()").extract()
        print("next2-------$$$$$$$"+ ", ".join(titles2))
        # pass
