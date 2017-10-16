# template for json
json_template = {
	"GetSetBuiltAt": 0,
	"additionalFeatures": {
		"characteristics": {
			"has_wheelchair_access": False,
			"managerie": False,
			"new_building": False,
			"pets": False,
			"share": False
		},
		"energy": {
			"eClass": "",
			"eConsumption": ""
		},
		"equipment": {
			"airConditioning": False,
			"barbecue": False,
			"cableTv": False,
			"ceramicHob": False,
			"dishwasher": False,
			"isdn": False,
			"steamOven": False,
			"tumbleDryer": False,
			"washingMachine": False
		},
		"exterior": {
			"balcony": False,
			"barbecue": False,
			"childFriendly": False,
			"lift": False,
			"parkingSpace": False,
			"playground": False,
			"pool": False,
			"privateGarage": False
		},
		"heating": {
			"electrical": False,
			"fuel": False,
			"gas": False,
			"pump": False,
			"solar": False,
			"wood": False
		},
		"interior": {
			"attic": False,
			"cellar": False,
			"fireplace": False,
			"hobbyRoom": False,
			"parquet": False,
			"pool": False,
			"sauna": False,
			"storageRoom": False,
			"view": False,
			"wineCellar": False
		}
	},
	"address": {
		"city": "",
		"street": "",
		"zipCode": 0
	},
	"countryCode": "CH",
	"details": {
		"availableAt": 0,
		"builtAt": 0,
		"description": "",
		"keywords": "",
		"renovatedAt": ""
	},
	"distances": {
		"busStation": 0,
		"highway": 0,
		"kindergarden": 0,
		"playground": 0,
		"primarySchool": 0,
		"proximity": {
			"lake": False,
			"mountains": False,
			"sea": False
		},
		"secondarySchool": 0,
		"shopping": 0,
		"trainStation": 0,
		"university": 0
	},
	"isRent": False,
	"isSale": False,
	"lat": 0,
	"lon": 0,
	"mainFeatures": {
		"baths": 0,
		"floor": 0,
		"floorSpace": 0,
		"floors": 0,
		"garages": 0,
		"livingSpace": 0,
		"lotSize": 0,
		"parkings": 0,
		"roomHeight": 0,
		"rooms": 0,
		"showers": 0,
		"toilets": 0,
		"volume": 0
	},
	"media": {
		"gallery": []
	},
	"name": "",
	"price": {
		"currency": "CHF",
		"expenses": 0,
		"rentNetPrice": 0,
		"rentPrice": 0,
		"rentUnit": 0,
		"salePrice": 0
	},
	"timeStampAdded": "",
	"categories": [],
	"isSpider": True,
	"spiderName": "urbanhome",
	"origSource": "source url goes here"
}

# payload dictionary containing values for valid request
payload = {
    "settings": {
        "MainTypeGroup": "1",
        "Category": "1",
        "AdvancedSearchOpen": False,
        "MailID": "",
        "PayType": "1",
        "Type": "1",
        "RoomsMin": "0",
        "RoomsMax": "0",
        "PriceMin": "0",
        "PriceMax": "0",
        "Regions": [],
        "SubTypes": ["0"],
        "SizeMin": "0",
        "SizeMax": "0",
        "Available": "",
        "NoAgreement": False,
        "FloorRange": "0",
        "RentalPeriod": "0",
        "equipmentgroups": [],
        "Email": "",
        "Interval": "0",
        "SubscriptionType1": True,
        "SubscriptionType2": True,
        "SubscriptionType4": True,
        "SubscriptionType8": True,
        "SubscriptionType128": True,
        "SubscriptionType512": True,
        "Sort": "0"
    },
    "manual": False,
    "skip": 0,
    "reset": True,
    "position": 0,
    "iframe": 0,
    "defaultTitle": True,
    "saveSettings": True
}

# request headers dictionary
request_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '639',
    'Content-Type': 'application/json; charset=UTF-8;',
    'Host': 'www.urbanhome.ch',
    'Origin': 'http://www.urbanhome.ch',
    'Referer': 'http://www.urbanhome.ch/search/rent/living/apartment/zh/winterthur',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# dictionary for selecting type of estate
type = {
    "apartment": 1,
    "apartment-share": 2,
    "house": 4,
    "parking": 8,
    "property": 128,
    "vacation home": 512
}

# dictionary with equipment keys
additional_features_dict = {
    "Cable TV": "cableTv:equipment",
    "Kabel TV": "cableTv:equipment",
    "Parking": "parkingSpace:exterior",
    "Parkplatz": "parkingSpace:exterior",
    "Pets allowed": "pets:characteristics",
    "Haustiere ok": "pets:characteristics",
    "Glass ceramic": "ceramicHob:equipment",
    "Glaskeramik": "ceramicHob:equipment",
    "Balcony": "balcony:exterior",
    "Balkon ": "balcony:exterior",
    "Dishwasher": "washingMachine:equipment",
    "Geschirrspüler": "washingMachine:equipment",
    "Garage": "privateGarage:exterior",
    "ISDN": "isdn:equipment",
    "Elevator": "lift:exterior",
    "Lift": "lift:exterior",
    "Underground parking": "parkingSpace:exterior",
    "Tiefgarage": "parkingSpace:exterior",
    "Flat share ok": "share:characteristics",
    "WG erlaubt": "share:characteristics",
    "Single garage": "privateGarage:exterior",
    "Einzelgarage": "privateGarage:exterior",
    "Wheelchair": "has_wheelchair_access:characteristics",
    "Rollstuhlgängig": "has_wheelchair_access:characteristics",
    "Renovated": "new_building:characteristics",
    "Renoviert": "new_building:characteristics",
    "Far view": "view:interior",
    "Weitsicht": "view:interior",
    "Childfriendly": "childFriendly:exterior",
    "Kinderfreundlich": "childFriendly:exterior",
	"Swimmingpool": "pool:exterior",
    "Parquet": "parquet:interior",
    "Parkett": "parquet:interior",
    "New building": "new_building:characteristics",
    "Neubau": "new_building:characteristics",
    "Tumbler": "tumbleDryer:equipment",
    "tumbleDryer": "tumbleDryer:equipment",
    "Playground": "playground:exterior",
    "Spielplatz": "playground:exterior",
    "Cellar": "cellar:interior",
    "Keller": "cellar:interior",
    "Oil": "fuel:heating",
    "Öl": "fuel:heating",
    "Dachterrasse": "balcony:exterior",
    "Erdgas": "gas:heating",
    "Talsicht": "view:interior",
    "Doppelgarage": "privateGarage:exterior",
    "Cheminée": "fireplace:interior",
    "Bergsicht": "view:interior",
    "Terrasse": "balcony:exterior"
}

main_features_dict = {
    "Badewanne": "baths",
    "WC": "toilets",
    "Dusche": "showers",
    "Balkon": "balcony"
}
