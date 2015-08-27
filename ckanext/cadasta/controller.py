import ckan.lib.base as base
import ckan.lib.helpers as helpers
from pylons import request
from ckan.controllers.package import PackageController
render = base.render
from ckan.lib.base import c
import model
from ckan.common import OrderedDict, _, json, request, c, g, response
from ckan.lib.search import SearchError

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.maintain as maintain
import ckan.lib.i18n as i18n
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.accept as accept
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.plugins as p
import ckan.lib.render
import cadasta_model
from datetime import datetime
from dateutil.parser import parse




NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin


def get_surveys():
    surveys=[1,2,3,4,5,6,4,6]
    return surveys


def _encode_params(params):
    return [(k, v.encode('utf-8') if isinstance(v, basestring) else str(v))
            for k, v in params]


def url_with_params(url, params):
    params = _encode_params(params)
    return url + u'?' + urlencode(params)


def search_url(params, package_type=None):
    if not package_type or package_type == 'dataset':
        url = h.url_for(controller='package', action='search')
    else:
        url = h.url_for('{0}_search'.format(package_type))
    return url_with_params(url, params)




class Cadasta_Controller(PackageController):


    def read(self, id):

        all_parcels = cadasta_model.get_all_parcels(id)
        activity_list = cadasta_model.get_cadasta_activity(id)


        if activity_list:
            for activity in activity_list['features']:


                reformatted_date = parse(activity['properties']['time_created'])
                reformatted_date = reformatted_date.strftime("%m/%d/%y")

                activity['properties']['time_created'] = reformatted_date


        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/read.html',
                      extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels, 'activity_list': activity_list})



    def read_parcels(self, id):

        # todo this is uniocde, what format does this need to be in to push it back to db
        # geom = request.params.get('parcel_geom')

        #get filter params
        filterArg = request.params.get('filter')

        #get sort params
        sortArg = request.params.get('sort')

        #if filters exist, ask API to filter parcels and respond
        parcel_list = cadasta_model.list_parcels(id, filter=filterArg, sort=sortArg)

        if parcel_list is not None and parcel_list['features'] is not None:
            for parcel in parcel_list['features']:

                reformatted_date = parse(parcel['properties']['time_created'])
                reformatted_date = reformatted_date.strftime("%m/%d/%y")

                parcel['properties']['time_created'] = reformatted_date

            

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/parcels.html',
                      extra_vars={'dataset_type': package_type, 'parcel_list': parcel_list, 'filter': request.params.get('filter'), 'sort': request.params.get('sort')})




    def form_data_upload(self, id):

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/form_data_upload.html',
                      extra_vars={'dataset_type': package_type})



    def new_parcel(self, id):

        new_parcel = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/edit_parcel_details.html',
                      extra_vars={'dataset_type': package_type, 'new_parcel': new_parcel})



    def read_parcel_details(self, id, parcel_id):

        parcel_geom = cadasta_model.get_parcel_geom(id)
        relationship_list = cadasta_model.list_relationships(id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id},
                                       package_type=package_type)

        return render('package/parcel_details.html',
                          extra_vars={'dataset_type': package_type, 'parcel_geom': parcel_geom, 'relationship_list':relationship_list})




    def edit_parcel_details(self, id, parcel_id):

        parcel_details = cadasta_model.get_parcel_details(parcel_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id},
                                       package_type=package_type)

        return render('package/edit_parcel_details.html',
                          extra_vars={'dataset_type': package_type, 'parcel_details': parcel_details})



    def show_parcel_map (self, id, parcel_id):

        all_parcels = cadasta_model.get_parcel_geom(id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels, 'parcel_id':parcel_id })



    def edit_parcel_map (self, id, parcel_id):

        all_parcels = cadasta_model.get_parcel_geom(id)
        edit = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels, 'edit':edit, 'parcel_id':parcel_id })



    def new_parcel_map (self, id):

        all_parcels = cadasta_model.get_parcel_geom(id)
        new = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels, 'new':new })



    def read_survey_details(self, id, survey_id):

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'survey_id' : survey_id},
                                       package_type=package_type)

        return render('package/survey_details.html',
                          extra_vars={'dataset_type': package_type})




    def edit_survey_details(self, id, survey_id):

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'survey_id' : survey_id},
                                       package_type=package_type)

        return render('package/edit_survey_details.html',
                          extra_vars={'dataset_type': package_type})



    def read_person_details(self, id, person_id):

        person = cadasta_model.get_person_details(person_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'person_id' : person_id},
                                       package_type=package_type)

        return render('package/person_details.html',
                          extra_vars={'dataset_type': package_type, 'person':person})



    def edit_person_details(self, id, person_id):

        newPerson = False

        person_details = cadasta_model.get_person_details(person_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'person_id' : person_id},
                                       package_type=package_type)

        return render('package/edit_person.html',
                          extra_vars={'dataset_type': package_type, 'newPerson': newPerson, 'person_details': person_details})



    def new_person(self, id):

        newPerson = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/edit_person.html',
                          extra_vars={'dataset_type': package_type, 'newPerson': newPerson})



    def show_map(self, id):

        all_parcels = cadasta_model.get_all_parcels(id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'

        self._setup_template_variables(context, {'id': id },
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels})


    def edit_map(self, id):

        all_parcels = cadasta_model.get_all_parcels(id)
        edit = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'

        self._setup_template_variables(context, {'id': id },
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'all_parcels': all_parcels, 'edit':edit})



    def show_surveys(self, id):

        ctype, format = self._content_type_from_accept()

        survey_list = cadasta_model.get_all_surveys(id)

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/surveys.html',
                          extra_vars={'dataset_type': package_type, 'survey_list': survey_list})




    def read_survey_templates(self, id):

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        return render('package/survey_template.html',
                          extra_vars={'dataset_type': package_type})


    #
    # def read_media(self, id):
    #
    #     ctype, format = self._content_type_from_accept()
    #
    #     response.headers['Content-Type'] = ctype
    #
    #     context = {'model': model, 'session': model.Session,
    #                'user': c.user or c.author, 'for_view': True,
    #                'auth_user_obj': c.userobj}
    #     data_dict = {'id': id, 'include_tracking': True}
    #
    #
    #     # check if package exists
    #     try:
    #         c.pkg_dict = get_action('package_show')(context, data_dict)
    #         c.pkg = context['package']
    #     except NotFound:
    #         abort(404, _('Dataset not found'))
    #     except NotAuthorized:
    #         abort(401, _('Unauthorized to read package %s') % id)
    #
    #     package_type = c.pkg_dict['type'] or 'dataset'
    #
    #     self._setup_template_variables(context, {'id': id},
    #                                    package_type=package_type)
    #
    #     return render('package/media.html',
    #                       extra_vars={'dataset_type': package_type})
    #



    def read_relationship_details(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'relationship':relationship})



    def edit_relationship_details(self, id, parcel_id, relationship_id):

        relationship_details = cadasta_model.get_relationship_details(relationship_id)

        new_relationship = False

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id' : parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/edit_relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'relationship_details': relationship_details, 'new_relationship': new_relationship})



    def new_relationship(self, id, parcel_id):

        new_relationship = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id},
                                       package_type=package_type)

        return render('package/edit_relationship_details.html',
                          extra_vars={'dataset_type': package_type, 'new_relationship':new_relationship })




    def show_relationship_map(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'relationship':relationship, 'relationship_id':relationship_id})



    def edit_relationship_map(self, id, parcel_id, relationship_id):

        relationship = cadasta_model.get_relationship_details(relationship_id)
        edit = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id, 'relationship_id': relationship_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'relationship': relationship, 'relationship_id':relationship_id, 'edit':edit})




    def new_relationship_map(self, id, parcel_id):

        new = True

        ctype, format = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id, 'include_tracking': True}


        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        package_type = c.pkg_dict['type'] or 'dataset'
        self._setup_template_variables(context, {'id': id, 'parcel_id': parcel_id},
                                       package_type=package_type)

        return render('package/map.html',
                          extra_vars={'dataset_type': package_type, 'id':id, 'parcel_id': parcel_id, 'new': new})


def search(self):

        package_type = self._guess_package_type()

        try:
            context = {'model': model, 'user': c.user or c.author,
                       'auth_user_obj': c.userobj}
            check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        # unicode format (decoded from utf8)
        q = c.q = request.params.get('q', u'')
        c.query_error = False
        page = self._get_page_number(request.params)

        limit = g.datasets_per_page

        # most search operations should reset the page counter:
        params_nopage = [(k, v) for k, v in request.params.items()
                         if k != 'page']

        def drill_down_url(alternative_url=None, **by):
            return h.add_url_param(alternative_url=alternative_url,
                                   controller='package', action='search',
                                   new_params=by)

        c.drill_down_url = drill_down_url

        def remove_field(key, value=None, replace=None):
            return h.remove_url_param(key, value=value, replace=replace,
                                  controller='package', action='search')

        c.remove_field = remove_field

        sort_by = request.params.get('sort', None)
        params_nosort = [(k, v) for k, v in params_nopage if k != 'sort']

        def _sort_by(fields):
            """
            Sort by the given list of fields.

            Each entry in the list is a 2-tuple: (fieldname, sort_order)

            eg - [('metadata_modified', 'desc'), ('name', 'asc')]

            If fields is empty, then the default ordering is used.
            """
            params = params_nosort[:]

            if fields:
                sort_string = ', '.join('%s %s' % f for f in fields)
                params.append(('sort', sort_string))
            return search_url(params, package_type)

        c.sort_by = _sort_by
        if not sort_by:
            c.sort_by_fields = []
        else:
            c.sort_by_fields = [field.split()[0]
                                for field in sort_by.split(',')]

        def pager_url(q=None, page=None):
            params = list(params_nopage)
            params.append(('page', page))
            return search_url(params, package_type)

        c.search_url_params = urlencode(_encode_params(params_nopage))

        try:
            c.fields = []
            # c.fields_grouped will contain a dict of params containing
            # a list of values eg {'tags':['tag1', 'tag2']}
            c.fields_grouped = {}
            search_extras = {}
            fq = ''
            for (param, value) in request.params.items():
                if param not in ['q', 'page', 'sort'] \
                        and len(value) and not param.startswith('_'):
                    if not param.startswith('ext_'):
                        c.fields.append((param, value))
                        fq += ' %s:"%s"' % (param, value)
                        if param not in c.fields_grouped:
                            c.fields_grouped[param] = [value]
                        else:
                            c.fields_grouped[param].append(value)
                    else:
                        search_extras[param] = value

            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author, 'for_view': True,
                       'auth_user_obj': c.userobj}

            if package_type and package_type != 'dataset':
                # Only show datasets of this particular type
                fq += ' +dataset_type:{type}'.format(type=package_type)
            else:
                # Unless changed via config options, don't show non standard
                # dataset types on the default search page
                if not asbool(config.get('ckan.search.show_all_types', 'False')):
                    fq += ' +dataset_type:dataset'

            facets = OrderedDict()

            default_facet_titles = {
                    'organization': _('Organizations'),
                    'groups': _('Groups'),
                    'tags': _('Tags'),
                    'res_format': _('Formats'),
                    'license_id': _('Licenses'),
                    }

            for facet in g.facets:
                if facet in default_facet_titles:
                    facets[facet] = default_facet_titles[facet]
                else:
                    facets[facet] = facet

            # Facet titles
            for plugin in p.PluginImplementations(p.IFacets):
                facets = plugin.dataset_facets(facets, package_type)

            c.facet_titles = facets

            data_dict = {
                'q': q,
                'fq': fq.strip(),
                'facet.field': facets.keys(),
                'rows': limit,
                'start': (page - 1) * limit,
                'sort': sort_by,
                'extras': search_extras
            }

            query = get_action('package_search')(context, data_dict)
            c.sort_by_selected = query['sort']

            c.page = h.Page(
                collection=query['results'],
                page=page,
                url=pager_url,
                item_count=query['count'],
                items_per_page=limit
            )
            c.facets = query['facets']
            c.search_facets = query['search_facets']
            c.page.items = query['results']
        except SearchError, se:
            log.error('Dataset search error: %r', se.args)
            c.query_error = True
            c.facets = {}
            c.search_facets = {}
            c.page = h.Page(collection=[])
        c.search_facets_limits = {}
        for facet in c.search_facets.keys():
            try:
                limit = int(request.params.get('_%s_limit' % facet,
                                               g.facets_default_number))
            except ValueError:
                abort(400, _('Parameter "{parameter_name}" is not '
                             'an integer').format(
                                 parameter_name='_%s_limit' % facet
                             ))
            c.search_facets_limits[facet] = limit

        maintain.deprecate_context_item(
          'facets',
          'Use `c.search_facets` instead.')

        self._setup_template_variables(context, {},
                                       package_type=package_type)

        return render('read_base.html',
                      extra_vars={'dataset_type': package_type})
