# coding=utf-8

###################################
# Standard library import
###################################

import warnings

##################################
# Third party library import
##################################

import requests


class Api(object):
    """A python interface into the Twitter API

    By default, the Api caches results for 1 minute.

    Example usage:
      To create an instance of the twitter.Api class, with no authentication:
        >>> import newsapi
        >>> api = newsapi.Api()
    """

    DEFAULT_CACHE_TIMEOUT = 60  # cache for 1 minute

    def __init__(self,
                 api_key=None,
                 input_encoding=None,
                 request_headers=None,
                 cache=DEFAULT_CACHE_TIMEOUT,
                 base_url=None,
                 version=None,
                 debugHTTP=False,
                 use_gzip_compression=False,
                 timeout=20,
                 proxies=None):

        self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
        self._input_encoding = input_encoding
        self._use_gzip = use_gzip_compression
        self._debugHTTP = debugHTTP
        self._shortlink_size = 19
        self._timeout = timeout
        self.__auth = None
        self._api_key = None

        self.proxies = proxies

        if not base_url:
            self.base_url="https://newsapi.org"

        if version == 2 or version == None:
            self.version=2
            self.base_url += "/v2/"
        elif version == 1:
            self.version=1
            self.base_url += "/v1/"

        endpoints = self.__SetEndpoints(self.version)

        self.__endpoints=endpoints

        if debugHTTP:
            import logging
            import http.client

            http.client.HTTPConnection.debuglevel = 1

            logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def SetCredentials(self,
                       api_key,
                       ):
        """
        Function to set the credentials

        Parameters
        ----------

        api_key: str
            API key from News API org; visit https://newsapi.org/sources
            for information.

        Returns
        -------

        self
        """
        self._api_key = api_key


    def __SetEndpoints(self,
                     version):
        """
        Function to set the endpoints based on the version

        Parameters
        ----------

        version: int (default 2)
            Integer representing News API version; choose between 1 and 2

        Returns
        -------

        endpoints: dict
            Returns a dictionary with the endpoints as values.
        """

        if version==2:
            endpoints = {"heads":'top-headlines?',"search":'everything?',"source":'sources?'}
        elif version==1:
            endpoints = {"search":'articles?',"source":'sources?'}

        return endpoints

    def getheadlines(self,
                     category=None,
                     language=None,
                     country=None,
                     sources=None,
                     keywords=None,
                     apiKey=None,
                     version=None):
        """

        Search all the headlines.

        Parameters
        -----------

        sources: str
            A comma seperated string of identifiers (maximum 20) for the news
            sources or blogs you want headlines from.  For a list of sources,
            visit the https://newsapi.org/sources

        keywords: str
            Keywords or phrase to search headlines for.

        category: str
            The category you want to get headlines for.  Options include,
            business, entertainment, gaming, general, health-and-medical,
            music, politics, science-and-nature, sport, technology.  Default
            returns all categories.

        language: str
            The 2-letter ISO-639 code of the language you want to get headlines
            for.  Options include ar, en, cn, de, es, fr, he, it, etc.  Visit
            https://www.loc.gov/standards/iso639-2/php/code_list.php for more
            information.

        country: str
            The 2-letter ISO 3166-1 code of the country you want to get
            headlines for.  Possible options are ar, au, br, ca, cn, de, etc.
            Visit https://en.wikipedia.org/wiki/ISO_3166-1 for details.

        apiKey: str
            Your API key; visit https://newsapi.org for details.
        """
        # set sources to first in index by default
        if not sources:
            sources = 'abc-news'

        # get version and raise error if not 2
        version=self.version
        if self.version != 2:
            raise ValueError('You must use Version 2 to retrieve headlines from'
                             ' News API service.')

        # retrive the api key if set; otherwise, error
        if not self._api_key:
            raise ValueError(
                'You must use use an API key; to get a key visit https://news'
                'api.org/. If you have an API key, set it using the '
                'Api.SetCredentials method.')

        # if api key is there, set the params
        else:
            request_params = {
                          "category": category,
                          'language': language,
                          "country": country,
                           "sources":sources,
                          "apiKey": self._api_key,
                          "q":keywords
                            }

        # build the url
        url = self.base_url + self.__endpoints['heads']

        # make the request
        r = requests.get(url,params=request_params,timeout=self._timeout)

        # return the json
        return r.json()

    def getsources(self,
                     category='general',
                     language=None,
                     country='us',
                     apiKey=None,
                     version=None):
        """
        Search all the sources provided by News API.

        Parameters
        -----------


        category: str
            Find sources that display news in this category. Options include
            business, technology, general, sport, politics, entertainment,
            gaming, health-and-medical, music, science-and-nature.

        language: str
            The 2-letter ISO-639 code of the language you want to get sources
            for.  Options include ar, en, cn, de, es, fr, he, it, etc.  Visit
            https://www.loc.gov/standards/iso639-2/php/code_list.php for more
            information.

        country: str
            The 2-letter ISO 3166-1 code of the country you want to get
            sources for.  Possible options are ar, au, br, ca, cn, de, etc.
            Visit https://en.wikipedia.org/wiki/ISO_3166-1 for details.

        apiKey: str
            Your API key; visit https://newsapi.org for details.
        """

        if self.version != 2:

            request_params = {
                "category":category,
                "language": language,
                "country":country,
                "apiKey": self._api_key,
            }

        # retrive the api key if set; otherwise, error
        if not self._api_key:
            raise ValueError(
                'You must use use an API key; to get a key visit https://news'
                'api.org/. If you have an API key, set it using the '
                'Api.SetCredentials method.')

        # if api key is there, set the params
        else:
            request_params = {
                          "category": category,
                          'language': language,
                          "country": country,
                          "apiKey": self._api_key,
                            }


        # build the url
        url = self.base_url + self.__endpoints['source']

        # make the request
        r = requests.get(url,params=request_params,timeout=self._timeout)


        # return the json
        return r.json()

    def searchnews(self,
                     keywords=None,
                     dateStart=None,
                     dateEnd=None,
                     sortBy=None,
                     domains=None,
                     page=20,
                     sources='abc-news',
                     language=None,
                     apiKey=None,
                     version=None):
        """
        Searches news in version 1 and version 2

        Parameters
        -----------

        dateStart: str
            A date and optional time for the oldest article allowed.  This
            should be in ISO 8601 format (e.g. 2017-11-20 or
            2017-11-20T02:13:37) Default: the oldest according to your plan.

        dateEnd: str
            A date and optional time for the newest article allowed.  This
            should be in ISO 8601 format (e.g. 2017-11-20 or
            2017-11-20T02:13:37) Default: the newest according to your plan.

        keywords: str
            Keywords or phrase to search for. Advanced search is supported
            so you can use quotes around phrases, prepend words that must appear
            with a + sign e.g. +bitcoin, prepend words that must not appear
            with a - sign e.g. -bitcoin, or use the AND/OR/NOT logical
            operators with grouping using parentheses.

        sources: str
            A comma seperated string of identifiers (maximum 20) for the news
            sources or blogs you want headlines from.  For a list of sources,
            visit the https://newsapi.org/sources

        domain: str
            A comman-seperated string of domains (e.g. bbc.co.uk,
            techcrunch.com, engadget.com, etc.) to restrict the search to.

        language: str
            The 2-letter ISO-639 code of the language you want to get articles
            for.  Options include ar, en, cn, de, es, fr, he, it, etc.  Visit
            https://www.loc.gov/standards/iso639-2/php/code_list.php for more
            information.
        sortBy: str
            The order to sort the articles in.  Possible options: relevancy,
            popularity, publishedAt.  Defaults to publishedAt.

        page: int
            Use this to page through the results. 20 page articles are returned
            on a page.

        country: str
            The 2-letter ISO 3166-1 code of the country you want to get
            headlines for.  Possible options are ar, au, br, ca, cn, de, etc.
            Visit https://en.wikipedia.org/wiki/ISO_3166-1 for details.

        apiKey: str
            Your API key; visit https://newsapi.org for details.
        """

        # detect version
        version = self.version
        request_params=None

        # set up for version 1 articles
        if self.version != 2:
            if sortBy not in ['top','latest','popular']:
                sortBy='top'
                warnings.warn('Version 1 sorts by top, latest, or popular. '
                              'Defaulted to top for this search.')

            request_params = {
                "sortBy":sortBy,
                "source": sources,
                "apiKey": self._api_key,
            }

        if not keywords and self.version !=1:
            raise ValueError('You must enter a keywords to use the search '
                             'service.')

        # retrive the api key if set; otherwise, error
        if not self._api_key:
            raise ValueError(
                'You must use use an API key; to get a key visit https://news'
                'api.org/. If you have an API key, set it using the '
                'Api.SetCredentials method.')

        # if api key is there, set the params
        else:
            if not request_params:
                if not sortBy:
                    if sortBy not in ['publishedAt', 'relevancy', 'popularity']:
                        sortBy='publishedAt'
                        warnings.warn('Version 2 can only sort by publishedAt, '
                                      'relevancy, or popularity.  Defaulted to '
                                      'publishedAt for this search.')
                request_params = {
                                 "q": keywords,
                                 "dateStart":dateStart,
                                 "dateEnd":dateEnd,
                                 "sortBy":sortBy,
                                 "domains":domains,
                                 "page":page,
                                 "sources":sources,
                                 "language":language,
                                 "apiKey": self._api_key,
                                }


        # build the url
        url = self.base_url + self.__endpoints['search']

        # make the request
        r = requests.get(url,params=request_params,timeout=self._timeout)

        print(r.url)
        # return the json
        return r.json()





