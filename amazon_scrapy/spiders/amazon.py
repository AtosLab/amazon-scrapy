# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from lxml import html
from scrapy import log
from lxml import etree

import unicodedata
from amazon_scrapy.items import AmazonScrapyItem

import csv
import sys

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'http://www.amazon.com/',
    )
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["am_asin", "am_name", "am_stock", "am_price", "am_price_shipping", "am_condition", "am_delivery"],
    }

    def __init__(self):
    	self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    def parse(self, response):

    	asin_lists = []
    	name_lists = []
    	with open('All6.csv') as csvfile:
    		readCSV = csv.reader(csvfile, delimiter=',')
    		for row in readCSV:
    			print(row[0])
    			print(row[1])
    			asin_lists.insert(len(asin_lists), row[0])
    			name_lists.insert(len(name_lists), row[1])

    	time.sleep(5)

    	self.driver.get(response.url)

    	time.sleep(5)

    	amazon_url = "http://www.amazon.com/"
    	asin_index = 0
    	for asin_item in asin_lists:
    		self.driver.get(amazon_url)
    		time.sleep(1)
    		twotabsearchtextbox = self.driver.find_element_by_id("twotabsearchtextbox")
    		twotabsearchtextbox.send_keys(asin_item)
    		form = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form')
    		form.submit()
    		time.sleep(1)

    		asin_index += 1
    		try:
    			my_item = AmazonScrapyItem()
    			my_item['am_asin'] = asin_item
    			my_item['am_name'] = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[4]/div[1]/div/ul/li/div/div/div/div[2]/div[1]/div[1]/a/h2").text.encode("utf-8")
    			my_item['am_stock'] = 1
    			my_item['am_price'] = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[4]/div[1]/div/ul/li/div/div/div/div[2]/div[2]/div[1]/div/div/a/span[2]").text.replace('$','').encode("utf-8")
    			

    			products_list = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[4]/div[1]/div/ul/li/div/div/div/div[2]/div[2]/div[1]/div/div/a")
    			products_list.click()
    			
    			#yield my_item
    			time.sleep(1)

    			#my_item = AmazonScrapyItem()
		        source = self.driver.page_source.encode("utf8")
		        tree = etree.HTML(source)
		        items = tree.xpath("//div[contains(@class, 'a-row a-spacing-mini olpOffer')]")

		        am_condition = ''
		        for item in items:

		      #   	my_item['am_asin'] = ''
	    			# my_item['am_name'] = ''
	    			# my_item['am_stock'] = ''
	    			# my_item['am_price'] = ''
		      #   	my_item['am_price_shipping'] = str(item.xpath("div[1]/span/text()") ).replace('[', '').replace(']','').replace("'", '').replace('$','').strip()

		      #   	my_item['am_condition'] = str(item.xpath("div[2]/div/span/text()") ).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()
		        	am_condition = str(item.xpath("div[2]/div/span/text()") ).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()
		        	if am_condition != 'New':
		        		break

		        if am_condition == 'New':
		        	my_item['am_stock'] = 0
		        	my_item['am_price'] = -1

		        yield my_item
    			time.sleep(1)
		      #   	deliverys = item.xpath("div[3]/ul/li")
		      #   	my_item['am_delivery'] = ''
		      #   	for delivery in deliverys:
		      #   		#my_item['am_delivery'] += str(delivery.xpath("span/text()") ).replace('[', '').replace(']','').replace("'", '').replace("\\n",'').strip()
		      #   		delsplit = str(delivery.xpath("span/text()")).split(",")

		      #   		del_index = 0
		      #   		print 'ccccccccccccccccccccccccccccccccccccccc'
		      #   		print len(delsplit)
		      #   		print str(delivery.xpath("span/text()"))
		      #   		while del_index < (len(delsplit)-1):
		      #   			my_item['am_delivery'] += str(delsplit[del_index]).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()

		      #   			if len(delsplit) == 2:
		      #   				my_item['am_delivery'] += str(delivery.xpath("span/a/text()")).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()
		      #   			else:
		      #   				my_item['am_delivery'] += str(delivery.xpath("span/a[" + str(del_index + 1) + "]/text()")).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()
		      #   			del_index += 1
		      #   		my_item['am_delivery'] += str(delsplit[del_index]).replace('[', '').replace(']','').replace("'", '').replace('\n','').replace("\\n",'').replace('$','').strip()
		      #   		print 'dddddddddddddddddddddddddddddddddddddddd'

		      #   	yield my_item
    				# time.sleep(1)

    		except:
    			print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    			my_item = AmazonScrapyItem()
    			my_item['am_asin'] = asin_item
    			my_item['am_name'] = name_lists[asin_index - 1]
    			my_item['am_stock'] = 0
    			my_item['am_price'] = -1
    			yield my_item
    			time.sleep(1)

    		

    	time.sleep(10)

        pass
