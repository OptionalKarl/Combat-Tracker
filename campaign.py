import json
from campaign_queries import insert_campaign;

class Campaign:
    def __init__(self, ID, campaign_token = None, name = None, setting = None, description = None):
        if name is not None and len(name) > 32:
            raise ValueError("Name exceeds maximum length of 32 characters")
        if setting is not None and len(name) > 32:
            raise ValueError("Name exceeds maximum length of 32 characters")    

        self.campaign_token = campaign_token
        self.name = name
        self.setting = setting
        self.description = description

    def create(self,data):
        try:
            campaign_data = json.loads(data)
            campaign = Campaign(**campaign_data)
        except ValueError:
            return [500, "Data items not valid"]
        except Exception as e:
            return [500, str(e)]
        
            insert_campaign(campaign)
            return [200,'"message": "Campaign created successfully"']
        except Exception as e:
           return [500, str(e)]    