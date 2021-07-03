# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import expose, BaseView as AppBuilderBaseView


ge_root_path = "/opt/airflow/"

# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "ge_bp", __name__,
    template_folder=f'{ge_root_path}great_expectations/uncommitted/data_docs/local_site',
    static_folder='static',
    static_url_path='/')


# Creating a flask appbuilder BaseView
class GreatExpectationsView(AppBuilderBaseView):
    default_view = "test"

    @expose("/")
    def test(self):
        return self.render_template("index.html")

    @expose("/<path:path>")
    def val(self, path):
        return self.render_template(f"{path}")


v_appbuilder_view = GreatExpectationsView()
v_appbuilder_package = {"name": "Validations",
                        "category": "Great Expectations",
                        "view": v_appbuilder_view}


# Defining the plugin class
class AirflowGEPlugin(AirflowPlugin):
    name = "ge_plugin"
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
