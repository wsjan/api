# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:40:26 2019

@author: Wojciech
"""
#%%
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.requests import Request
# from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pandas as pd
from sqlite3 import connect
from wykres import create_plot

#%%
def is_browser(request):
    browser_useragents = ["ABrowse", "Acoo Browser", "America Online Browser", "AmigaVoyager", "AOL", "Arora", "Avant Browser", "Beonex", "BonEcho", "Browzar", "Camino", "Charon", "Cheshire", "Chimera", "Chrome", "ChromePlus", "Classilla", "CometBird", "Comodo_Dragon", "Conkeror", "Crazy Browser", "Cyberdog", "Deepnet Explorer", "DeskBrowse", "Dillo", "Dooble", "Edge", "Element Browser", "Elinks", "Enigma Browser", "EnigmaFox", "Epiphany", "Escape", "Firebird", "Firefox", "Fireweb Navigator", "Flock", "Fluid", "Galaxy", "Galeon", "GranParadiso", "GreenBrowser", "Hana", "HotJava", "IBM WebExplorer", "IBrowse", "iCab", "Iceape", "IceCat", "Iceweasel", "iNet Browser", "Internet Explorer", "iRider", "Iron", "K-Meleon", "K-Ninja", "Kapiko", "Kazehakase", "Kindle Browser", "KKman", "KMLite", "Konqueror", "LeechCraft", "Links", "Lobo", "lolifox", "Lorentz", "Lunascape", "Lynx", "Madfox", "Maxthon", "Midori", "Minefield", "Mozilla", "myibrow", "MyIE2", "Namoroka", "Navscape", "NCSA_Mosaic", "NetNewsWire", "NetPositive", "Netscape", "NetSurf", "OmniWeb", "Opera", "Orca", "Oregano", "osb-browser", "Palemoon", "Phoenix", "Pogo", "Prism", "QtWeb Internet Browser", "Rekonq", "retawq", "RockMelt", "Safari", "SeaMonkey", "Shiira", "Shiretoko", "Sleipnir", "SlimBrowser", "Stainless", "Sundance", "Sunrise", "surf", "Sylera", "Tencent Traveler", "TenFourFox", "theWorld Browser", "uzbl", "Vimprobable", "Vonkeror", "w3m", "WeltweitimnetzBrowser", "WorldWideWeb", "Wyzo", "Android Webkit Browser", "BlackBerry", "Blazer", "Bolt", "Browser for S60", "Doris", "Dorothy", "Fennec", "Go Browser", "IE Mobile", "Iris", "Maemo Browser", "MIB", "Minimo", "NetFront", "Opera Mini", "Opera Mobile", "SEMC-Browser", "Skyfire", "TeaShark", "Teleca-Obigo", "uZard Web", "Thunderbird", "AbiLogicBot", "Link Valet", "Link Validity Check", "LinkExaminer", "LinksManager.com_bot", "Mojoo Robot", "Notifixious", "online link validator", "Ploetz + Zeller", "Reciprocal Link System PRO", "REL Link Checker Lite", "SiteBar", "Vivante Link Checker", "W3C-checklink", "Xenu Link Sleuth", "EmailSiphon", "CSE HTML Validator", "CSSCheck", "Cynthia", "HTMLParser", "P3P Validator", "W3C_CSS_Validator_JFouffa", "W3C_Validator", "WDG_Validator", "Awasu", "Bloglines", "everyfeed-spider", "FeedFetcher-Google", "GreatNews", "Gregarius", "MagpieRSS", "NFReader", "UniversalFeedParser", "!Susie", "Amaya", "Cocoal.icio.us", "DomainsDB.net MetaCrawler", "gPodder", "GSiteCrawler", "iTunes", "lftp", "MetaURI", "MT-NewsWatcher", "Nitro PDF", "Snoopy", "URD-MAGPIE", "WebCapture", "Windows-Media-Player"]
    if any(browser_useragent in request.headers['user-agent'] for browser_useragent in browser_useragents):
        return True
    else:
        return False

#%%
class WielkosciPodstawowe(BaseModel):
    data : List[datetime] 
    krajowe_zapotrzebowanie_na_moc : List[float] 
    sumaryczna_generacja_JWCD : List[float]
    generacja_PI : List[float]
    generacja_IRZ : List[float]
    sumaryczna_generacja_nJWCD : List[float] 
    krajowe_saldo_wymiany_międzysystemowej_równoległej : List[float] 
    krajowe_saldo_wymiany_międzysystemowej_nierównoległej : List[float] 

#%%
# templates = Jinja2Templates(directory='')
app = FastAPI()

@app.get('/wielkosci_podstawowe', response_model=WielkosciPodstawowe)
async def wielkosci_podstawowe(request: Request, format: str = None,
start: str = None, end: str = None):
    '''  '''
    con = connect('pse.sqlite')

    if start is None and end is None:
        df = pd.read_sql('''select * from wielkosci_podstawowe''', con)
    elif start is None and end is not None:
        df = pd.read_sql('''select * from wielkosci_podstawowe where 
        Data <= '{}' '''.format(end), con)
    elif start is not None and end is None:
        df = pd.read_sql('''select * from wielkosci_podstawowe where 
        Data >= '{}' '''.format(start), con)
    elif start is not None and end is not None:
        df = pd.read_sql('''select * from wielkosci_podstawowe where 
        Data BETWEEN '{}' AND '{}' '''.format(start, end), con)
         
    browser = is_browser(request)

    if not browser or format == 'json':
        df.columns = df.columns.map(lambda x: x[0].lower() + x[1:]).str.replace(' ', '_') 
        return df.reset_index().to_dict(orient='list')

    elif browser or format == 'browser':
        create_plot(df)
        return HTMLResponse(open('wykres.html', encoding='utf-8').read())
#%%
