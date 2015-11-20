/*
* AmigoProxy
*
* Copyright (c) 2011-2015 AmigoCloud Inc., All rights reserved.
*
* This library is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public
* License as published by the Free Software Foundation; either
* version 3.0 of the License, or (at your option) any later version.
*
* This library is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* Lesser General Public License for more details.
*
* You should have received a copy of the GNU General Public
* License along with this library.
*/

function initTypeahead (objects, element, emptyMsg, limit) {
    emptyMsg = emptyMsg || 'No matches';
    var theEngine = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: objects,
        limit: limit || 5
    });
    theEngine.initialize();
    $(element).typeahead({
        hint: false,
        highlight: true,
        minLength: 1
    }, {
        name: 'theEngine',
        displayKey: 'name',
        source: theEngine.ttAdapter(),
        templates: {empty: '<div style="padding:5px 20px">' + emptyMsg + '<div>'}
    });
}
