######################################################################################################################
#  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                    #
#  Licensed under the Apache License Version 2.0 (the "License"). You may not use this file except in compliance     #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://www.apache.org/licenses/                                                                               #
#                                                                                                                    #
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

import os

from configuration.config_dynamodb_adapter import ConfigDynamodbAdapter
from configuration.scheduler_config_builder import SchedulerConfigBuilder

# environment parameter for configuration table
ENV_CONFIG = "CONFIG_TABLE"
ENV_STATE = "STATE_TABLE"
ENV_ACCOUNT = "ACCOUNT"
ENV_STACK = "STACK_NAME"
ENV_TAG_NAME = "TAG_NAME"
ENV_SCHEDULE_FREQUENCY = "SCHEDULER_FREQUENCY"
ENV_TRACE = "TRACE"
ENV_USER_AGENT = "USER_AGENT"
ENV_SCHEDULER_RULE = "SCHEDULER_RULE"

# name of months
MONTH_NAMES = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
# name of weekdays
WEEKDAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# values for switching automation off or on, first value is converted to false, the second to true
SWITCH_VALUES = ['off', 'on']

# default timezone for scheduler
DEFAULT_TZ = "UTC"

# default tag name
DEFAULT_TAGNAME = "Schedule"

# format for time in configurations
TIME_FORMAT_STRING = "%H:%M"

# trace flag
TRACE = "trace"

# metrics flag
METRICS = "use_metrics"

# regions
REGIONS = "regions"

# starttime
BEGINTIME = "begintime"
# description of a running period
DESCRIPTION = "description"
# name of the default timezone setting
DEFAULT_TIMEZONE = "default_timezone"
# endtime
ENDTIME = "endtime"
# type of instance
INSTANCE_TYPE = "instancetype"
# days in month the instance is running
MONTHDAYS = "monthdays"
# months instance is running
MONTHS = "months"
# name of a period or schedule
NAME = "name"
# name of the overwrite setting, legacy use
OVERWRITE = "overwrite"
# name of the overrride setting to set starte to constantly running or stopped
OVERRIDE_STATUS = "override_status"
# running periods section
PERIODS = "periods"
# running period configuration
PERIOD = "period"
# running schedules section
SCHEDULES = "schedules"
# name of scheduled services
SCHEDULED_SERVICES = "scheduled_services"
# schedule RDS Multi-AZ ans Autora Clusters
SCHEDULE_CLUSTERS = "schedule_clusters"
# create snapshot before stopping RDS Instances
CREATE_RDS_SNAPSHOT = "create_rds_snapshot"
# stop new instances
STOP_NEW_INSTANCES = "stop_new_instances"
# use maintenance windows
USE_MAINTENANCE_WINDOW = "use_maintenance_window"
# ssm maiantenance windows to use for EC2
SSM_MAINTENANCE_WINDOW = "ssm_maintenance_window"
# name of timezone setting for a schedule
TIMEZONE = "timezone"
# name of the tagname setting
TAGNAME = "tagname"
# days in a week the instance is running
WEEKDAYS = "weekdays"
# cross_account_roles_arn_list
CROSS_ACCOUNT_ROLES = "cross_account_roles"
# process instances in account in which lambda function is installed
SCHEDULE_LAMBDA_ACCOUNT = "schedule_lambda_account"
# enforce schedule state
ENFORCED = "enforced"
# use hibernation for stopped instances
HIBERNATE = "hibernate"
# retain running instances at end of period if they were already running at beginning of period
RETAINED_RUNNING = "retain_running"
# started and stopped tags, these are set to started and stoped instances
STARTED_TAGS = "started_tags"
STOPPED_TAGS = "stopped_tags"
# stack id for "child" stacks to create schedules in the configuration of a scheduler stack
SCHEDULE_CONFIG_STACK = "configured_in_stack"

OVERRIDE_STATUS_STOPPED = "stopped"
OVERRIDE_STATUS_RUNNING = "running"
OVERRIDE_STATUS_VALUES = [OVERRIDE_STATUS_STOPPED, OVERRIDE_STATUS_RUNNING]

# used to separate period name from instance type
INSTANCE_TYPE_SEP = "@"

TAG_VAL_SCHEDULER = "scheduler"
TAG_VAL_MINUTE = "minute"
TAG_VAL_HOUR = "hour"
TAG_VAL_YEAR = "year"
TAG_VAL_MONTH = "month"
TAG_VAL_DAY = "day"
TAG_VAL_TIMEZONE = "timezone"

__configuration = None


def get_scheduler_configuration(logger):
    """
    Returns the scheduler configuration
    :return: scheduler configuration
    """
    global __configuration
    if __configuration is None:
        configdata = ConfigDynamodbAdapter(os.getenv(ENV_CONFIG)).config
        __configuration = SchedulerConfigBuilder(logger=logger).build(configdata)
        if logger is not None:
            logger.debug("Configuration loaded\n{}", str(__configuration))
    return __configuration


def unload_scheduler_configuration():
    """
    Force the configuration to unload
    :return:
    """
    global __configuration
    __configuration = None
