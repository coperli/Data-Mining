############################################################################################
#                                                                                          #
#      This code is written during team meet-up by team members as shown below ...         #
#                                                                                          #  
#                    WQD170042                                          #
#                    WQD180006                             #
#                    WQD180048                                  #
#                    WQD180066                                              #
#                    WQD180029                                          #
#                                                                                          #
############################################################################################

# Batch 1 

# Importing related Python modules/packages.
from lxml import html
from datetime import datetime
import requests
import pymysql


# List of companies that listed in KLSE Main Board.
companies = (
'ADVENTA','AHEALTH','HARTA','IHH','KOSSAN','KOTRA','KPJ','PHARMA','SUPERMX',
'TMCLIFE','TMCLIFE-WB','TOPGLOV','YSPSAH','ALAM','ARMADA','BARAKAH','CARIMIN','COASTAL','DAYA',
'DAYANG','DELEUM','DIALOG','HANDAL','HENGYUAN','HIBISCS','HIBISCS-WC','HUAAN','ICON','KNM',
'KNM-WB','MHB','PENERGY','PERDANA','PERISAI','PETRONM','REACH','REACH-WA','SAPNRG','SAPNRG-PA',
'SAPNRG-WA','SCOMI','SCOMI-WB','SCOMIES','SERBADK','SUMATEC','SUMATEC-WA','T7GLOBAL','THHEAVY','THHEAVY-PB',
'UZMA','VELESTO','VELESTO-WA','WASEONG','YINSON','CENSOF','CENSOF-WB','CUSCAPI','D%26O','DATAPRP',
'DIGISTA','DIGISTA-WB','DNEX','DNEX-WD','DSONIC','DSONIC-WA','EDARAN','EFORCE','EFORCE-WA','ELSOFT',
'FRONTKN','FSBM','FSBM-WA','GHLSYS','GRANFLO','GTRONIC','HTPADU','INARI','INARI-WB','ITRONIC',
'JCY','KESM','KEYASIC','MI','MMSV','MPI','MSNIAGA','MYEG','NOTION','NOTION-WC',
'OMESTI','PENTA','PRESBHD','THETA','TRIVE','TRIVE-WB','TURIYA','UNISEM','VITROX',
'VSTECS','WILLOW','ACME','AMPROP','AMPROP-PA','AMPROP-PB','AMVERTON','ARK','ARK-WB','ASIAPAC',
'ASIAPAC-WB','AYER','BCB','BDB','BERTAM','BJASSET','BJASSET-WB','CHHB','CHHB-WB','CRESNDO',
'CVIEW','DAIMAN','DBHD','DBHD-WA','DPS','DPS-WB','E%26O','E%26O-WB','ECOFIRS','ECOFIRS-WC',
'ECOWLD','ECOWLD-WA','ENCORP','ENRA','EUPE','EWEIN','EWINT','EWINT-WA','FARLIM','GLOMAC',
'GMUTUAL','GOB','GOB-WA','GSB','GUOCO','HCK','HCK-WA','HOOVER','HUAYANG','IBHD',
'IBHD-WA','IBRACO','IDEAL','IDEAL-WB','IGBB','IGBB-PA','IGBB-PB','IOIPG','IVORY','IWCITY',
'JIANKUN','JIANKUN-WA','JKGLAND','KBUNAI','KBUNAI-WC','KEN','KSL','L%26G','LBICAP','LBS',
'LBS-PA','LBS-WB','LIENHOE','MAGNA','MAGNA-WB','MAHSING','MAHSING-WC','MALTON','MATRIX','MATRIX-WA',
'MBWORLD','MCT','MEDAINC','MEDAINC-WA','MEDAINC-WB','MEDAINC-WC','MENANG','MENANG-WB','MJPERAK','MKH',
'MKLAND','MPCORP','MRCB','MRCB-WB','MUH','MUIPROP','NAIM','OIB','OSK','OSK-WC',
'PARAMON','PASDEC','PASDEC-WA','PHB','PLB','PLENITU','RAPID','SAPRES','SBCCORP','SDRED',
'SEAL','SHL','SIMEPROP','SMI','SNTORIA','SNTORIA-WA','SNTORIA-WB','SPB','SPSETIA','SPSETIA-PA',
'SPSETIA-PB','SUNSURIA','SUNSURIA-WA','SYMLIFE','SYMLIFE-WB','TADMAX','TAGB','TALAMT','TAMBUN','TANCO',
'TANCO-WB','THRIVEN','THRIVEN-WB','TIGER','TIGER-WC','TITIJYA','TITIJYA-PA','TROP','TROP-WA','UEMS',
'UOADEV','WMG','Y%26G','Y%26G-WA','YNHPROP','YONGTAI','YONGTAI-PA','YONGTAI-WA','YTLLAND','EDEN',
'EDEN-WB','GASMSIA','KPS','MALAKOF','MFCB','MFCB-WA','PBA','PETGAS','RANHILL','SALCON',
'SALCON-WB','TALIWRK','TENAGA','YTL','YTLPOWR','ABMB','AEONCR','AFFIN','ALLIANZ','ALLIANZ-PA',
'AMBANK','APEX','BIMB','BIMB-WA','BURSA','CIMB','ECM','ELKDESA','HLBANK','HLCAP',
'HLFG','INSAS','INSAS-PA','INSAS-WB','JOHAN','KENANGA','KUCHAI','LPI','MAA','MANULFE',
'MAYBANK','MBSB','MNRB','MPHBCAP','P%26O','PBBANK','RCECAP','RHBBANK','TA','TAKAFUL')

#'PANPAGE','
# Defining AppCrawler class that use to crawl stock data from the hardcoded weblink.
class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

# Crawled data            
        # Company name 
        stock_name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        
        # Company stock code in KLSE
        stock_code = tree.xpath('//li[@class="f14"]/text()')[1]
        
        # Stock open price of the day
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        
        # Stock high price of the day
        high_price = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        
        # Stock low price of the day
        low_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        
        # Stock last price of the day
        last_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        
        # Stock price change
        price_change_up = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"] //span[@class="quote_up"]/text()')
        price_change_down = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"] //span[@class="quote_down"]/text()')
        
        if len(price_change_up) == 0 and len(price_change_down) != 0:
            price_change = price_change_down[0]
        
        elif len(price_change_down) == 0 and len(price_change_up) != 0:
            price_change = price_change_up[0]
        
        elif len(price_change_down) == 0 and len(price_change_up) == 0:
            price_change = 0

        # Stock price change in percentage
        price_change_percent = tree.xpath('//td[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        
        # Stock volume
        stock_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        
        # Buy volume
        buy_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]

        # Sell volume
        sell_volume = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]


# Defining database connection that use to store crawled stock data together with the date of the stock price         
        connection = pymysql.connect(host='localhost', user='root', password='see26288', db='KLSE')
        cursor = connection.cursor()
        
        current_Date = datetime.now()
        formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
        #formatted_date = current_Date.strftime('%Y-%m-%d')
        
        insert_to_database = (stock_name, stock_code[3:], open_price, high_price, low_price, last_price, price_change, price_change_percent, stock_volume, buy_volume, sell_volume, formatted_date)
        
        sql = 'INSERT INTO Stock (stock_name, stock_code, open_price, high_price, low_price, last_price, price_change, price_change_percent, stock_volume, buy_volume, sell_volume, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, insert_to_database)	
        connection.commit()
         
        print('Company Name: ' + str(stock_name))
        print('Stock Code: ' + str(stock_code[3:]))
        print('Open Price: ' + str(open_price))
        print('High Price: ' + str(high_price))
        print('Low Price: ' + str(low_price))
        print('Last Price: ' + str(last_price))
        print('Price Change: ' + str(price_change))
        print('Price Change in %: ' + str(price_change_percent))
        print('Stock Volume: ' + str(stock_volume))
        print('Buy / Volume: ' + str(buy_volume))
        print('Sell / Volume: ' + str(sell_volume))
        print("Records were saved to database successfully\n\n")
	
        return


# Crawling of stock data for the companies that set in the listing 
# The crawling is based on the hardcoded weblink and AppCrawler class
for company in companies:
    weblink = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=' + str(company)
    crawler = AppCrawler(weblink, 0)
    crawler.crawl()
    
# End of the code
