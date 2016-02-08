/**
# Author:   Cory Nance <canance@coastal.edu>
# Revision: 6 February 2016
#
# Copyright 2016 Coastal Carolina University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 */

$(function () {
        $("#accordion").accordion({
            "heightStyle": "content",
        });
    $("input[type=submit]").button();
    $("#radio").buttonset();
    $("#configuration_select").buttonset();

    $("select[multiple=\"multiple\"]").multiSelect({
        selectableHeader: "<div class='select_header'>Available</div>",
        selectionHeader: "<div class='select_header'>Selected</div>",
    });

    $( "#tabs" ).tabs({
      beforeLoad: function( event, ui ) {
        ui.jqXHR.fail(function() {
          ui.panel.html(
            "Couldn't load this tab. We'll try to fix this as soon as possible.");
        });
      }
    });
});

