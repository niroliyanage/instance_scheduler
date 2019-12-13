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
import calendar

from configuration.setbuilders.setbuilder import SetBuilder


class WeekdaySetBuilder(SetBuilder):
    """
   Class to build sets for weekdays, 0-6 or Mon-Sun, day#n for nth occurrence of day in month, or L for last
   occurrence of the day for the month
    """
    WEEKDAY_NUMBER_CHAR = "#"
    LAST_DAY_WILDCARD = "L"

    def __init__(self, wrap=True, year=None, month=None, day=None, ignorecase=True):
        """

        :param wrap: Set to True to allow wrapping at last day of the week
        :param year: Year of week to build sets for, only required for date aware '#' and 'L' features in expressions
        :param month: Month of week to build sets for, only required for date aware '#' and 'L' features in expressions
        :param day:  Day in week to build sets for, only required for date aware '#' and 'L' features in expressions
        :param ignorecase: Set to True to ignore case when mapping day names to set values
        """
        SetBuilder.__init__(self,
                            names=calendar.day_abbr,
                            wrap=wrap,
                            ignorecase=ignorecase,
                            significant_name_characters=3,
                            last_item_wildcard=WeekdaySetBuilder.LAST_DAY_WILDCARD)
        self._year = year
        self._month = month
        self._day = day
        self._first_weekday_in_month = None
        self._days_in_month = None

        self._post_custom_parsers = [self._parse_name_number,  # name#num
                                     self._parse_value_number,  # value#num
                                     self._parse_name_last_weekday,  # nameL
                                     self._parse_value_last_weekday]  # valueL

    def _seperator_characters(self):
        # Add last day wildcard as it needs for formatting before parsing
        return SetBuilder._seperator_characters(
            self) + WeekdaySetBuilder.WEEKDAY_NUMBER_CHAR + self.LAST_DAY_WILDCARD

    # noinspection PyMethodParameters
    def _requires_date_attributes(fn):
        # this modifier is used to mark to use methods that need year, day and month which are optional for the builder
        def check(self, *args, **kwargs):
            if self._year is None or self._month is None or self._day is None:
                raise ValueError(
                    "year, month and day parameters must be specified when creating the {} for using method {}".format(
                        self.__class__.__name__, fn.__name__))

            # and if we're checking for the first time then get the first weekday and numbers for the month
            if self._first_weekday_in_month is None:
                self._first_weekday_in_month, self._days_in_month = calendar.monthrange(self._year, self._month)

            # noinspection PyCallingNonCallable
            return fn(self, *args, **kwargs)

        check.__name__ = fn.__name__
        return check

    # noinspection PyArgumentList,PyArgumentList
    @_requires_date_attributes
    def _parse_name_number(self, name_number_str):
        # weekday_name#occurence
        return self._get_occurrence_item(number_str=name_number_str, fn=self._get_value_by_name)

    # noinspection PyArgumentList,PyArgumentList
    @_requires_date_attributes
    def _parse_value_number(self, value_number_str):
        # weekday value# occurrence
        return self._get_occurrence_item(number_str=value_number_str, fn=self._get_value_by_str)

    def _get_occurrence_item(self, number_str, fn):
        # gets the nth occurrence of a weekday retrieved by function fn

        # check for separator
        temp = number_str.split(self.WEEKDAY_NUMBER_CHAR)
        # check for occurrence number and if it is valid
        if len(temp) == 2:
            try:
                number = int(temp[1])
            except ValueError:
                raise ValueError("Number value must be an integer value ({})".format(temp[1]))

            if number < 1 or number > 5:
                raise ValueError("Number value must be in range 1-5 ({})".format(temp[1]))

            # get the weekday
            weekday = fn(temp[0])
            if weekday is None:
                return None

            # gets the first occurrence of that weekday in the month
            day_for_number_weekday = self._get_day_for_first_occurrence_month(weekday)

            monthday = day_for_number_weekday + ((number - 1) * 7)
            return [weekday] if self._day == monthday else []

        return None

    def _get_day_for_first_occurrence_month(self, weekday):
        # calculated the first occurrence of a weekday in a month
        day = 1
        if weekday != self._first_weekday_in_month:
            day += (weekday - self._first_weekday_in_month) % 7
        return day

    # noinspection PyArgumentList,PyArgumentList
    @_requires_date_attributes
    def _parse_name_last_weekday(self, name_last_weekday):
        # nameL, returns last occurrence of weekday, specified by its name, in a month
        return self._get_last_day_for_weekday_in_month(name_last_weekday, self._get_value_by_name)

    # noinspection PyArgumentList,PyArgumentList
    @_requires_date_attributes
    def _parse_value_last_weekday(self, value_last_weekday):
        # valueL, returns last occurrence of weekday, specified by its value, string in a month
        return self._get_last_day_for_weekday_in_month(value_last_weekday, self._get_value_by_str)

    def _get_last_day_for_weekday_in_month(self, last_weekday_str, fn):
        # weekdayL, returns last occurrence of weekday, retrieved by function fn, string in a month
        if last_weekday_str.endswith(WeekdaySetBuilder.LAST_DAY_WILDCARD):
            weekday = fn(last_weekday_str[:-1])
            if weekday is not None:
                day_for_number_weekday = self._get_day_for_first_occurrence_month(weekday)
                while day_for_number_weekday + 7 <= self._days_in_month:
                    day_for_number_weekday += 7
                return [weekday] if day_for_number_weekday == self._day else []
