import ckan.lib.base as base
from pylons import request
from ckan.controllers.package import PackageController
render = base.render
from ckan.lib.base import c
import model
from ckan.common import OrderedDict, _, json, request, c, g, response

import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.plugins
import ckan.lib.render
import cadasta_model
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


class Parcel_Controller(PackageController):

    def read_parcels(self, id):

        # todo this is uniocde, what format does this need to be in to push it back to db
        # geom = request.params.get('parcel_geom')

        #get filter params
        filterArg = request.params.get('filter')

        #get sort params
        sortArg = request.params.get('sort')

        #if filters exist, ask API to filter parcels and respond
        parcel_list = cadasta_model.list_parcels(id, filter=filterArg, sort=sortArg)

        if parcel_list is not None and parcel_list.get("features", None) is not None:
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

        return render('package/parcel_details.html',
                          extra_vars={'dataset_type': package_type, 'parcel_geom': parcel_geom, 'relationship_list':relationship_list, 'parcel_details': parcel_details})




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



