"""
Function returns selected fields for a given Project entity in ShotGrid.
Returns data as JSON.

@author: Matt Clementson, matt.clementson@ibigroup.com
"""
__updated__ = '2022-04-13'

import logging
import shotgun_api3
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    project_id = req.params.get('project_id')
    if project_id:
        # Authenticate with ShotGrid as script
        sg = shotgun_api3.Shotgun("https://ibigroup.shotgunstudio.com",
                                script_name="desktopAutomationAccess",
                                api_key="lxyzrrb7of%knvsceguklLnzu")
        project_dat = {}

        if sg is not None:
            fields = ['name', 'sg_visialization_lead', 'sg_file_location',
                      'sg_bst_task_code', 'sg_project_number',
                      'sg_design_office', 'landing_page_url',
                      'sg_alternate_viz_lead_s']
            filters = [
                ["id", "is", int(project_id)]
            ]
            project_data = sg.find_one("Project", filters, fields)
            if project_data['sg_visialization_lead'] is not None:
                project_data["viz_lead_id"] = project_data['sg_visialization_lead']['id']
            json_output = json.dumps(project_data, indent=3)
            sg.close()
        return func.HttpResponse(json_output, status_code=200)

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a project ID in the query string or in the request body for a personalized response.",
             status_code=200
        )
