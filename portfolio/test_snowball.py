import unittest

from snowball import Snowball


class TestSnowball(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.snowball = Snowball()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_last_close(self):
        print(self.snowball.last_close('.INX'))

    def test_get_data(self):
        print(self.snowball.get_data('SPY', '2004-01-01'))

    def test_my_cvt_bones(self):
        print(self.snowball.my_cvt_bones())

    def test_postman(self):
        import requests

        url = "https://stock.xueqiu.com/v5/stock/quote.json?symbol=SH000985"

        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Cookie': 'Hm_lvt_1db88642e346389874251b5a1eded6e3=1724762463; __utma=1.1668734999.1691826037.1716164071.1716181419.14; __utmz=1.1691826037.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_r_token=e2035d2b526e0bb132171373fc5c0c7606dc13c7; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjQwMTEwMTczMTEsImlzcyI6InVjIiwiZXhwIjoxNzI3ODg5ODYyLCJjdG0iOjE3MjUyOTc4NjIxNTcsImNpZCI6ImQ5ZDBuNEFadXAifQ.hzq-_YtZbCr1D9WmIRP9X2Gaa16BRjn_jFDXZs4LTo9pvnaxM0LFZJyaImI7_Zm2OhpLm7aJU6CuK7P0vEmIGphL4KbkOeiPxrn1VqGwR7tRiwt3zBfHAiYYc9TfxI_pMuZQQoAQqwmIgutRmnI_50oNTH6FZ49eXybGz0CycXRHfOhWS2qt4f2tGLZySW6xpdoawVYcwyGvyebEYK9UwKEs6P9piW-CixXvK4RgyjguVsTzM5ktyZejLkp_osaDGL_nwG5us8TLW68Hj-IQIp61aPUsX0lekFbEUYtgmAtUOm54RNxuc3E-WrPPoIQh661x3eJJSBoR_A0U1sm4Pg; u=4011017311; xq_is_login=1; bid=eaa5e87aadbfc6538dd5598fd7f84ee1_lp10v6r2; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=Ab+j8vBiER5LmrQtmL9XtO/xFJOcUwzfi0NiVz5Y54MN+lgPB4qmdAQIwySGUEmUVsCaSM8Q8tFuNlfSBxgBXw%3D%3D; smidV2=20240327221700cd3c4b16b8ba074fe8dcfa6ed1428f7400613bbb509586e80; ssxmod_itna=iq+xuD9GvOqBPiKGdD7I25xCTeWTqRKrnFuw2w5DsezNDpxBKidDaxQcqZDDtaNDmuKeq90RTpWe4KEbL3V8PO0ubYFPoAhanteoTKD=xYQDwxYoODAqKD9zDr1kyDixGWDbxDYDi4DrMx0rDY5ODD5DAxi8Ix0CMaaPD0RzDlKhMgB+Dn9+UrKhLQykMEIOTGRTKDeEU6HOI65DNhuzDGczeChdNDed5iiNxaa4iW+5qehxx6D4ABree0e7ZAhX7HxDipxieYD=; ssxmod_itna2=iq+xuD9GvOqBPiKGdD7I25xCTeWTqRKrnFuwxikEeqYDlrBxmq03raYc60kzczKWuW3DwagPGcDYFPxD; device_id=8a9f975d14d4d1c759a9732259559a3c; cookiesu=861724027560412; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1725336714; HMACCOUNT=BAA45E0C43C05553; snbim_minify=true; s=c3127bpgp8; xq_a_token=31ccebd8e11c474dccc2efbf31bfc966be2032af; xqat=31ccebd8e11c474dccc2efbf31bfc966be2032af; acw_tc=2760827117253353698697145ea87f48737daebf85cb8b73c59f41560e4e7a; is_overseas=0'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)


if __name__ == '__main__':
    unittest.main()
