import time
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.core.management import call_command
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from .models import Executor
from .forms import ExecutorForm

scheduler = BlockingScheduler()
tz = pytz.timezone('America/New_York')


@admin.register(Executor)
class ExecutorModelAdmin(admin.ModelAdmin):
    form = ExecutorForm
    change_form_template = 'myapp/test_case_executor_form.html'
    list_display = ('id', 'status', 'start_time', 'end_time', 'error', 'app_name', 'test_case')
    readonly_fields = ('status', 'start_time', 'end_time', 'error')

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == 'POST':
            form = ExecutorForm(request.POST)
            if form.is_valid():
                self.run_test_case_with_apscheduler(request)
        extra_context = {'form': self.get_form(request), "add_view": True}
        return super(ExecutorModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)


    def change_view(self, request, object_id, form_url="", extra_context=None):
        execute = Executor.objects.get(id=object_id)
        form = self.get_form(request)(instance=execute)
        extra_context = {"form": form, "change_view": True}
        if request.method == 'POST':
            form = ExecutorForm(request.POST)
            if form.is_valid():
                self.run_test_case_with_apscheduler(request)
        return super(ExecutorModelAdmin, self).change_view(request, object_id, form_url=form_url,
                                                           extra_context=extra_context)

    @staticmethod
    def run_test_case_with_apscheduler(request):
        def run_test_cases():
            app_name = request.POST.get('app_name')
            command_list = request.POST.get('test_case')
            call_command(app_name, command_list)
            scheduler.shutdown(wait=False)

        # Schedule the function to run once, 2 minutes from now
        run_time = (datetime.now() + timedelta(seconds=2)).astimezone(pytz.utc)
        my_job = scheduler.add_job(run_test_cases, 'date', next_run_time=run_time, id='my_job_id')
        scheduler.start()


