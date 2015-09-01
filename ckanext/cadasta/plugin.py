import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins import IRoutes
from routes.mapper import SubMapper
import ckan.lib.plugins as lib_plugins
from ckan.lib.plugins import DefaultGroupForm




class CadastaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, DefaultGroupForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers) 

    # connect to API to get data about projects and parcels.  These are example functions to return some data


    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cadasta')

    def before_map(self, map):

        controller = 'ckanext.cadasta.controller:Cadasta_Controller'

        #new routes to be added

          #project
        map.connect('project_overview', '/project/{id}', controller=controller, action='read')
        map.connect('project_surveys', '/project/{id}/surveys', controller=controller, action='show_surveys')
        map.connect('project_parcels', '/project/{id}/parcels', controller=controller, action='read_parcels')
        map.connect('project_resources', '/project/{id}/resources', controller=controller, action='read_resources')
        map.connect('project_activity_stream', '/project/{id}/activity_stream', controller=controller, action='read_activity_stream')
        map.connect('project_survey_template', '/project/{id}/survey_template', controller=controller, action='read_survey_template')
        map.connect('project_form_data_upload', '/project/{id}/form_data_upload', controller=controller, action='form_data_upload')


          #big map
        map.connect('project_map', '/project/{id}/map', controller=controller, action='show_map')
        map.connect('edit_project_map', '/project/{id}/edit_map', controller=controller, action='edit_map')
        map.connect('show_parcel_map', '/project/{id}/parcel/{parcel_id}/map', controller=controller, action='show_parcel_map')
        map.connect('edit_parcel_map', '/project/{id}/edit_parcel/{parcel_id}/map', controller=controller, action='edit_parcel_map')
        map.connect('new_parcel_map', '/project/{id}/new/parcel/map', controller=controller, action='new_parcel_map')

        map.connect('show_relationship_map', '/project/{id}/parcel/{parcel_id}/relationship/{relationship_id}/map', controller=controller, action='show_relationship_map')
        map.connect('edit_relationship_map', '/project/{id}/parcel/{parcel_id}/edit_relationship/{relationship_id}/map', controller=controller, action='edit_relationship_map')
        map.connect('new_relationships_map', '/project/{id}/parcel/{parcel_id}/new/relationship/map', controller=controller, action='new_relationship_map')



          #parcels
        map.connect('parcel_details', '/project/{id}/parcel/{parcel_id}', controller=controller, action='read_parcel_details')
        map.connect('edit_parcel_details', '/project/{id}/edit_parcel/{parcel_id}', controller=controller, action='edit_parcel_details')
        map.connect('new_parcel', '/project/{id}/new/parcel', controller=controller, action='new_parcel')

          #surveys
        map.connect('survey_details', '/project/{id}/survey/{survey_id}', controller=controller, action='read_survey_details')
        map.connect('edit_survey_details', '/project/{id}/edit_survey/{survey_id}', controller=controller, action='edit_survey_details')

          #relationship
        map.connect('relationship_details', '/project/{id}/parcel/{parcel_id}/relationship/{relationship_id}', controller=controller, action='read_relationship_details')
        map.connect('edit_relationship_details', '/project/{id}/parcel/{parcel_id}/edit_relationship/{relationship_id}', controller=controller, action='edit_relationship_details')
        map.connect('new_relationship', '/project/{id}/parcel/{parcel_id}/new/relationship', controller=controller, action='new_relationship')

          #people/groups
        map.connect('person', '/project/{id}/person/{person_id}', controller=controller, action='read_person_details')
        map.connect('edit_person_details', '/project/{id}/edit_person/{person_id}', controller=controller, action='edit_person_details')
        map.connect('new_person', '/project/{id}/new/person', controller=controller, action='new_person')


        #remapping routes from dataset to project

        map.redirect('/dataset/{url:.*}', '/project/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/dataset', '/project',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/datasets/{url:.*}', '/project/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/datasets', '/project',
                     _redirect_code='301 Moved Permanently')


        map.redirect('/group/{url:.*}', '/organization/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/group', '/organization',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/groups/{url:.*}', '/organization/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/groups', '/organization',
                     _redirect_code='301 Moved Permanently')




        # package_controller = 'ckan.controllers.package:PackageController'

        with SubMapper(map, controller='package') as m:
            #define what is happening at each route using the package controller and the given action

            m.connect('/new/project', action='new')
            # m.connect('/project/{id}', action='read')
            m.connect('/project/{id}.{format}', action='read')

            m.connect('/project', action='search')

            m.connect('/project/edit/{id}', action='edit')

            m.connect('/project/activity/{id}', action='activity')

            m.connect('/project/resources/{id}', action='resources')

            m.connect('/project/{id}/resource/{resource_id}', action='resource_read')
            m.connect('/project/{id}/resource_delete/{resource_id}', action='resource_delete')
            m.connect('/project/{id}/resource_edit/{resource_id}', action='resource_edit')
            m.connect('/project/{id}/resource/{resource_id}/download', action='resource_download')
            m.connect('/project/{id}/resource/{resource_id}/download/{filename}', action='resource_download')
            m.connect('/project/{id}/resource/{resource_id}/embed', action='resource_embedded_dataviewer')
            m.connect('/project/{id}/resource/{resource_id}/preview/{preview_type}', action='resource_datapreview')


            m.connect('/project/{action}/{id}',
                      requirements=dict(action='|'.join([
                          'new_resource',
                          'history',
                          'read_ajax',
                          'history_ajax',
                          'follow',
                          'activity',
                          'groups',
                          'unfollow',
                          'delete',
                          'api_data',
                      ])))

        return map


    def after_map(self, map):
        return map


    #adding in new package schema
    def _modify_package_schema(self, schema):
        schema.update({
            'cadasta_id': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
                'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
                })
        return schema

    def create_package_schema(self):
        schema = super(CadastaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(CadastaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(CadastaPlugin, self).show_package_schema()
        schema.update({
            'cadasta_id': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema['resources'].update({
                'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
            })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []


    def get_helpers(self):
	return { }


    # #user schema update
    # def _modify_user_schema(self, schema):
    #     schema.update({
    #         'phone': [toolkit.get_validator('ignore_missing'),
    #                         toolkit.get_converter('convert_to_extras')]
    #     })
    #     return schema
    #
    # def create_user_schema(self):
    #     schema = super(CadastaPlugin, self).create_user_schema()
    #     schema = self._modify_user_schema(schema)
    #     return schema
    #
    # def update_user_schema(self):
    #     schema = super(CadastaPlugin, self).update_user_schema()
    #     schema = self._modify_user_schema(schema)
    #     return schema
    #
    #
    #
    # #
    # def is_fallback(self):
    #     # Return True to register this plugin as the default handler for
    #     # package types not handled by any other IDatasetForm plugin.
    #     return True
    #
    # def package_types(self):
    #     # This plugin doesn't handle any special package types, it just
    #     # registers itself as the default (above).
    #     return []
    #
    #
    # def get_helpers(self):
    #     return { }
    #
    #
    # plugins.implements(plugins.IGroupForm, inherit=True)
    # plugins.implements(plugins.IConfigurer)
    #
    # ## IGroupForm
    #
    #
    # def group_types(self):
    #     return ['organization']
    # #
    # def form_to_db_schema_options(self, options):
    #     ''' This allows us to select different schemas for different
    #     purpose eg via the web interface or via the api or creation vs
    #     updating. It is optional and if not available form_to_db_schema
    #     should be used.
    #     If a context is provided, and it contains a schema, it will be
    #     returned.
    #     '''
    #     schema = options.get('context', {}).get('schema', None)
    #     if schema:
    #         return schema
    #
    #     if options.get('api'):
    #         if options.get('type') == 'create':
    #             return self.form_to_db_schema_api_create()
    #         else:
    #             return self.form_to_db_schema_api_update()
    #     else:
    #         return self.form_to_db_schema()
    #
    #
    # def form_to_db_schema(self):
    #     schema = super(CadastaPlugin, self).form_to_db_schema()
    #     schema = self._modify_group_schema(schema)
    #     return schema
    #
    # def _modify_group_schema(self, schema):
    #
    #     # Import core converters and validators
    #     _convert_to_extras = plugins.toolkit.get_converter('convert_to_extras')
    #     _ignore_missing = plugins.toolkit.get_validator('ignore_missing')
    #
    #     default_validators = [_ignore_missing, _convert_to_extras, unicode]
    #     schema.update({
    #         'publisher_source_type': default_validators,
    #         'publisher_iati_id': default_validators
    #     })
    #
    #     return schema
    #
    # def db_to_form_schema(self):
    #
    #     # Import core converters and validators
    #     _convert_from_extras = plugins.toolkit.get_converter('convert_from_extras')
    #     _ignore_missing = plugins.toolkit.get_validator('ignore_missing')
    #     _ignore = plugins.toolkit.get_validator('ignore')
    #     _not_empty = plugins.toolkit.get_validator('not_empty')
    #
    #     schema = super(CadastaPlugin, self).form_to_db_schema()
    #
    #     default_validators = [_convert_from_extras, _ignore_missing]
    #     schema.update({
    #         'publisher_source_type': default_validators,
    #         'publisher_iati_id': default_validators
    #     })
    #
    #     return schema
