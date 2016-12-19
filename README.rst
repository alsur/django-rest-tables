Django REST Tables
##################
Create dynamic tables with Angular using your Django Rest Framework API.

If you use Django Rest Framework, get a representation of your results dynamic and easy to use and extend. Features
include:

* Self-construction.
* Pagination.
* Filter by columns.
* Sort by columns.
* Change the field representation.

Basic usage
===========

Create a table class including your Django Rest Framework (DRF) ViewSet:

.. code-block:: python

    # myapp/api.py
    # ------------
    class MyTable(Table):
        class Meta:
            view_set = MymodelViewSet  # DRF ViewSet


Add it to your view context:

.. code-block:: python

    # myapp/views.py
    # --------------
    def my_view(request):
        return render(request, 'myapp/mytable.html', {'table': MyTable()})


Add it to your template:

.. code-block:: htmldjango

    {# myapp/templates/myapp/mytable.html #}
    {# ---------------------------------- #}

    {% load rest_tables %}

    {% rest_table table %}

    ....
    <script src="//unpkg.com/angular@1.3.12/angular.min.js" type="text/javascript"></script>
    <script src="//unpkg.com/ng-table@3.0.1/bundles/ng-table.min.js" type="text/javascript"></script>
    <script src="{% static 'rest_tables/src/js/rest_tables.js' %}" type="text/javascript"></script>


It's all!