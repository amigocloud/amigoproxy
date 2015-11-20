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

// Submit all delete forms (clicking on the trash or the X)
$('.delete-form').submit(function () {
    var $this = $(this);
    $.ajax({
        data: $this.serialize(),
        type: $this.attr('method'),
        url: $this.attr('action'),
        complete: function () {
            window.location.reload();
        }
    });
    return false;
});

// Clicking on edit target fills the target form
$('.targets .edit-item').click(function () {
    var parent = $(this).parent().parent();
    var form = $('.save-target');
    form.find('input[name="id"]').val($(this).attr('target-id'));
    form.find('input[name="name"]').val(parent.find('.target-name').text().trim());
    form.find('input[name="url"]').val(parent.find('.target-url').text().trim());
    form.find('.save-or-create').text('Save');
    form.find('input[name="name"]').focus();
    return false;
});

// Submit form: saves or creates target
$('.save-target').submit(function () {
    var $this = $(this);
    $.ajax({
        data: $this.serialize(),
        type: $this.attr('method'),
        url: $this.attr('action'),
        success: function (data) {
            window.location.reload();
        },
        error: function (data) {
            var error = $this.parent().find('.error-msg');
            error.html(data.responseText + '.');
            error.show();
        }
    });
    return false;
});

// When a source is selected, store the source id in the hidden input: name="id"
$('#source-name').bind('typeahead:selected', function (e, obj, name) {
    $('.source-search').find('input[name="id"]').val(obj.id);
});

// When submitting a source search, add it as a GET parameter and reload
$('.source-search').submit(function () {
    var source = $(this).find('input[name="id"]').val() || $('#source-name').val();
    window.location.replace(
        window.location.href.split('?')[0] + '?source=' + encodeURIComponent(source)
    );
    return false;
});

// When a group is selected, store the group id in the hidden input: name="id"
$('#group-name').bind('typeahead:selected', function (e, obj, name) {
    $('.add-group form').find('input[name="group_id"]').val(obj.id);
});

// Submit form: links a  group to an existing source
$('.add-group form').submit(function () {
    var $this = $(this);
    $.ajax({
        data: $this.serialize(),
        type: $this.attr('method'),
        url: $this.attr('action'),
        success: function (data) {
            window.location.reload();
        },
        error: function (data) {
            var error = $this.parent().find('.error-msg');
            error.html("You didn't select any valid group.");
            error.show();
        }
    });    
    return false;
});

// When a target is selected, store the target id in the input attribute: target-id
$('#target-name').bind('typeahead:selected', function (e, obj, name) {
    $(this).attr('target-id', obj.id);
});

// Template for group targets
var target_template = '<span class="new-target" target-id="{id}">{name} <a href=""><i class="fa fa-close"></i></a></span>';

// Clicking on the [+] button adds a new target to a new or existing group
$('#add-target').click(function () {
    var target = $('#target-name');
    if (!target.val()) {
        return false;
    }
    var group_targets = $('#group-targets'),
        new_target = target_template.replace('{name}', target.val())
                                    .replace('{id}', target.attr('target-id'));
    if (!group_targets.find('.new-target').length) {
        $('#no-targets').hide();
    }
    group_targets.append(new_target);
    target.val('');
    target.attr('target-id', '');
    return false;
});

// Clicking  on the X of a target removes it from the list of targets
$('#group-targets').on('click', 'a', function () {
    var span = $(this).parent();
    span.remove();
    if (!$('#group-targets').find('.new-target').length) {
        $('#no-targets').show();
    }
    return false;
});

// Clicking on edit group fills the group form
$('.groups .edit-item').click(function () {
    var parent = $(this).parent().parent(),
        form = $('.save-group'),
        group_targets = $('#group-targets'),
        new_target, count = 0;
    form.find('input[name="id"]').val($(this).attr('group-id'));
    form.find('input[name="name"]').val(parent.find('.group-name').text().trim());
    form.find('input[name="default"]').prop('checked', parent.find('.badge').text().search('All') == 0);
    // Add existing targets
    group_targets.find('.new-target').remove();
    parent.find('.existing-target').each(function () {
        new_target = target_template.replace('{name}', $(this).text().trim())
                                    .replace('{id}', $(this).attr('target-id'));
        group_targets.append(new_target);
        ++count;
    });
    if (count) {
        $('#no-targets').hide();
    } else {
        $('#no-targets').show();
    }
    form.find('.save-or-create').text('Save');
    form.find('input[name="name"]').focus();
    return false;
});

// Submit form: saves or creates a group (dumping all the selected targets)
$('.save-group').submit(function () {
    var $this = $(this),
        targets = [];
    $this.find('.new-target').each(function () {
        targets.push($(this).attr('target-id'));
    });
    var data = $this.serialize() + '&targets=' + targets.join(',');
    $.ajax({
        data: data,
        type: $this.attr('method'),
        url: $this.attr('action'),
        success: function (data) {
            window.location.reload();
        },
        error: function (data) {
            var error = $this.parent().find('.error-msg');
            error.html(data.responseText + '.');
            error.show();
        }
    });
    return false;
});
