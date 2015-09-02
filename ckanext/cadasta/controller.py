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



    def read_party_details(self, id, party_id):

        party = cadasta_model.get_party_details(party_id)

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
        self._setup_template_variables(context, {'id': id, 'party_id' : party_id},
                                       package_type=package_type)

        return render('package/party_details.html',
                          extra_vars={'dataset_type': package_type, 'party':party})



    def edit_party_details(self, id, party_id):

        newPerson = False

        party_details = cadasta_model.get_party_details(party_id)

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
        self._setup_template_variables(context, {'id': id, 'party_id' : party_id},
                                       package_type=package_type)

        return render('package/edit_party.html',
                          extra_vars={'dataset_type': package_type, 'newPerson': newPerson, 'party_details': party_details})



    def new_party(self, id):

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

        return render('package/edit_party.html',
                          extra_vars={'dataset_type': package_type, 'newPerson': newPerson})






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



    def read_resources(self, id):

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

        return render('package/resources.html',
                          extra_vars={'dataset_type': package_type})


    def read_activity_stream(self, id):

        ctype, format = self._content_type_from_accept()

        activity_list = cadasta_model.get_cadasta_activity(id)


        if activity_list:
            for activity in activity_list['features']:


                reformatted_date = parse(activity['properties']['time_created'])
                reformatted_date = reformatted_date.strftime("%m/%d/%y")

                activity['properties']['time_created'] = reformatted_date


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

        return render('package/activity_stream.html',
                          extra_vars={'dataset_type': package_type, 'activity_list': activity_list})

