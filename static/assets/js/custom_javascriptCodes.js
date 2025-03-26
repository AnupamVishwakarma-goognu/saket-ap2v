// $(document).ready(function() {
//     // Javascript method's body can be found in assets/js/demos.js
//     demo.initDashboardPageCharts();
//
//     demo.showNotification();
//
//     demo.initVectorMap();
//
// });

$('#update_courses').on('submit', function(e){
  e.preventDefault();
  // var update_c_form_data = $(this).serializeObject();
  var update_c_form_data = new FormData($(this)[0]);
  var post_url = $(this).attr('action');
  // console.log(update_c_form_data);
  swal({
      title: "Are you sure to Update Course!",
      text: "You will not be go back!",
      type: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, Update!",
      confirmButtonClass: "btn btn-info btn-fill",
      closeOnConfirm: false,
  }, function(){
    $.ajax({
      url: post_url,
      type: "POST",
      data: update_c_form_data,
      async: true,
      cache: false,
      contentType: false,
      enctype: 'multipart/form-data',
      processData: false,
      success: function(r){
        window.location.href = '/courses/list/';
      },
      error: function(r){
        window.location.href = '/courses/list/';
      }
        // if (r.status == 1) {
        //   swal({
        //     title: 'Good job!',
        //     text: 'The Course Successfully updated',
        //     type: 'success',
        //     showCancelButton: true,
        //     confirmButtonClass: "btn btn-info btn-fill",
        //     confirmButtonText: "Okay",
        //     cancelButtonClass: "btn btn-danger btn-fill",
        //     closeOnConfirm: false,
        //   }, function(CourseConfirm){
        //     if (CourseConfirm){
        //       window.location.href=r.redirect;
        //     } else {
        //       window.location.href=r.redirect;
        //     }
        //   })
        // } else {
        //   swal({
        //     title: 'WARNING to Update',
        //     text: 'This Course could not be update. (Contact to Admin)',
        //     type: 'warning',
        //     showCancelButton: true,
        //     confirmButtonClass: "btn btn-info btn-fill",
        //     confirmButtonText: "Okay",
        //     cancelButtonClass: "btn btn-danger btn-fill",
        //     closeOnConfirm: false,
        //   }, function(CourseConfirm){
        //     if (CourseConfirm){
        //       window.location.href=r.redirect;
        //     } else {
        //       window.location.href=r.redirect;
        //     }
        //   })
        // }
    });
  }
)
});

$('#AddCourses').on('submit', function(e){
  e.preventDefault();
  var c_from_data = new FormData($(this)[0]);
  var c_from_action = $(this).attr('action');
  $.ajax({
    url: c_from_action,
    type: 'POST',
    data: c_from_data,
    async: true,
    cache: false,
    contentType: false,
    enctype: 'multipart/form-data',
    processData: false,
    success: function(response){
     console.log(response);
    },
    error: function(response){
     console.log("Error");
    }
  });
});

$('#new_instructor_form').on('submit', function(e){
  e.preventDefault();
  var instructor_form_data = $(this).serializeObject();
  var instructor_from_action = $(this).attr("action");
  $.ajax({
    type: "POST",
    url: instructor_from_action,
    data: instructor_form_data,
    success: function(response){
      if(response.result == true){
        demo.showInstuctorFromCreated()
        $("#new_instructor_form").trigger('reset')
      } else {
          swal({
              title: "Error To created Instructor!",
              text: "Okay => Refresh Page, Close => Refill Again.",
              type: "warning",
              showCancelButton: true,
              cancelButtonClass: "btn btn-danger btn-fill",
              closeOnConfirm: false,
          }, function(inconfirm) {
              if (inconfirm) {
                window.location.href = window.location.href;
              }
        });
      }
    },
    error: function(response){
      swal({
          title: "Error To created Instructor!",
          text: "Okay => Refresh Page, Close => Refill Again.",
          type: "warning",
          showCancelButton: true,
          cancelButtonClass: "btn btn-danger btn-fill",
          closeOnConfirm: false,
      }, function(inconfirm) {
          if (inconfirm) {
            window.location.href = window.location.href;
          }
      });
    }
  });
});

$("#update_enquiry").on('submit', function(e){
  e.preventDefault();
  var e_update_data = $(this).serialize();
  var e_update_data_f_action_url = $(this).attr("action");
  $.ajax({
    type: "POST",
    url: e_update_data_f_action_url,
    data: e_update_data,
    success: function(response){
      if(response.result == true){
        window.location.href = window.location.href;
      } else {
        demo.showSwal('update_error')
      }
    },
    error: function(response){
      demo.showSwal('update_error')
    }
  });
});

function AccordingFunction(enquiry_id, followups_id){
  $.ajax({
    type: "GET",
    url: "/followups/followup_add_details",
    data: {
      "enquiry_id": enquiry_id
    },
    success: function(response){
      var accordion_get_by_id = $('#accordion');
      $("#modal_accordion_form").attr('action', '/enquiries/followups/' + response[0].enquiry_id + "/");
      for (i = 0; i < response.length; i++){
        var followup_next_followup = response[i].next_followup;
        var followup_mode = response[i].followup_mode;
        var followup_response = response[i].response;
        var followup_comment = response[i].comments;
        var followup_addon_date = response[i].added_on;
        accordion_get_by_id.append(`<div class="card"><div class="card-header"><h4 class="card-title"><a data-target="#collapse${i}" href="#" data-toggle="collapse" class="collapsed" aria-expanded="false">${followup_addon_date}(${followup_mode})<b class="caret"></b></a></h4></div><div id="collapse${i}" class="card-collapse collapse"><div class="card-body"><p>${followup_comment}</p></div></div></div>`)
      }
    },
    error: function(response){
      console.log("Error")
    }
  });
};

$('#followupModel').on('hidden.bs.modal', function(){
  window.location.href = window.location.href;
});

$('#modal_accordion_form').on('submit', function(e){
  e.preventDefault();
  var action_url = $(this).attr('action');
  var model_accrodion_from_data = $(this).serialize();
  $.ajax({
    type: "POST",
    url: action_url,
    data: model_accrodion_from_data,
    success: function(response){
      if(response.result == true){
        location.reload();
      }
    },
    error: function(response){
      location.reload();
    }
  });
});

/*
var DataTable_var = $("#datatables").dataTable({
        "paging": false,
        "searching": false,
        "pageLength": 25,
        "sDom": "f",
        "ordering": true,
        "info": true,
        "autoWidth": true,
        "bFilter": false,
      });
*/

function search_filter_function(s_data){
  var s_data_value = s_data.value;
  if (s_data_value.length != 0){
    $.ajax({
      type: "GET",
      url: "/enquiries/table_data_filter",
      data: {
        "filter_data": s_data_value
      },
      success: function(response){
        DataTable_var.fnClearTable();
        for (i = 0; i < response.length; i++){
          data = [];
          var response_id = response[i].id;
          var response_mobile = response[i].mobile;
          var response_fullname = response[i].full_name;
          var response_reference = response[i].reference;
          var response_branch_location = response[i].branch_location;
          var response_email = response[i].email;
          data.push(response_id,response_fullname,response_email,response_mobile,response_branch_location,response_reference);
          DataTable_var.fnAddData(data);
          // $('tr[role="row"]')[response_id].setAttribute('onclick', 'window.location.href="/enquiries/view/${response_id}/";')
          var row_value = i;
          $('tr[role="row"]')[row_value+=1].onclick = function(){
            window.location.href="/enquiries/view/"+response_id
          };
        }
      },
      errorlog: function(response){
        alert("Error");
      }
    });
  } else {
    window.location.href = window.location.href;
  }
};

$("#search_type").on('change', function(e){
  var search_type_value = $(this).val();
  var protocol_var = $(location).attr('protocol') + "//";
  var domain_host = protocol_var + $(location).attr('host');
  if (search_type_value == "mobile"){
    $('#search_form').attr('action', domain_host + "/mobile/")
  } else if (search_type_value == "name"){
    $('#search_form').attr('action', domain_host + "/name/")
  } else if (search_type_value == "email"){
    $('#search_form').attr('action', domain_host + "/email/")
  } else if (search_type_value == "course"){
    $('#search_form').attr('action', domain_host + "/course/")
  } else if (search_type_value == "followup"){
    $('#search_form').attr('action', domain_host + "/followup/")
  } else if (search_type_value == "enquiries"){
    $('#search_form').attr('action', domain_host + "/enquiries/enquiries_filter")
  }
});

$(document).ready(function() {
    demo.checkFullPageBackgroundImage();

    setTimeout(function() {
        // after 1000 ms we add the class animated to the login/register card
        $('.card').removeClass('card-hidden');
    }, 400)
});

var $table = $('#bootstrap-table');

function operateFormatter(value, row, index) {
    return [
        '<a rel="tooltip" title="Edit" class="btn btn-link btn-warning table-action edit" href="javascript:void(0)">',
        '<i class="fa fa-edit"></i>',
        '</a>',
        '<a rel="tooltip" title="Remove" class="btn btn-link btn-danger table-action remove" href="javascript:void(0)">',
        '<i class="fa fa-remove"></i>',
        '</a>'
    ].join('');
}

$(document).ready(function() {
    window.operateEvents = {
     'click .edit': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click edit icon, row: ', info);
            console.log(info);
        },
        'click .remove': function(e, value, row, index) {
            console.log(row);
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
        }
    };

    $table.bootstrapTable({
        toolbar: ".toolbar",
        clickToSelect: true,
        showRefresh: true,
        search: true,
        showToggle: true,
        showColumns: true,
        pagination: true,
        searchAlign: 'right',
        pageSize: 8,
        clickToSelect: false,
        pageList: [8, 10, 25, 50, 100],

        formatShowingRows: function(pageFrom, pageTo, totalRows) {
            //do nothing here, we don't want to show the text "showing x of y from..."
        },
        formatRecordsPerPage: function(pageNumber) {
            return pageNumber + " rows visible";
        },
        icons: {
            refresh: 'fa fa-refresh',
            toggle: 'fa fa-th-list',
            columns: 'fa fa-columns',
            detailOpen: 'fa fa-plus-circle',
            detailClose: 'fa fa-minus-circle'
        }
    });

    //activate the tooltips after the data table is initialized
    $('[rel="tooltip"]').tooltip();

    $(window).resize(function() {
        $table.bootstrapTable('resetView');
    });


});

$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
});

$('#add_course_form').on('submit', function(e) {
  e.preventDefault();
  var add_course_data = $(this).serializeObject();
  var add_course_url = $(this).attr('action');
  $.ajax({
    type: "POST",
    url: add_course_url,
    data: {
      courseid: add_course_data.courseid,
      enquiry_id: enquiry__id
    }, success: function(response){
      window.location.href = window.location.href
    }
  });
});

/* ---Enquiry form javascript start here--- */
$(document).on('submit', '#new_enquiry_form', function(e){
    e.preventDefault();

    var enq = $('#new_enquiry_form').serializeObject();

/* ---console is used for debugging purpose at browser--- */
    var bd = '';
    var course = '';
    if(Array.isArray(enq.course)){
      for(var i = 0; i<enq.course.length; i++){
          if(i === 0){
          course += enq.course[i];
          }
          else{
              course += ',' + enq.course[i];
          }
      }
    }
    else{
      course=enq.course;
    }
    if(enq.select_days){
      for(var i = 0; i<enq.select_days.length; i++){
        if (Object.prototype.toString.call( enq.select_days ) == '[object Array]') {
          if(i === 0){
              bd += enq.select_days[i];
          }
          else{
              bd += ',' + enq.select_days[i];
          }
        } else {
          bd += enq.select_days;
          break;
        }
      }
      console.log(bd);
      console.log(enq.select_days.length, enq.select_days);
      
    }
    mobile = enq.con_code+"#"+enq.mobile
    $.ajax({
            type:'POST',
            url :'/enquiries/',
            data :{
                reference: enq.reference,
                fullname: enq.fullname,
                email: enq.email,
                mobile: mobile,
                company: enq.company,
                designation: enq.designation,
                course: course,
                select_days: bd,
                assigned_by: enq.assigned_by,
                interested_batch:enq.interested_batch,
                enquiry_level: enq.enquiry_level,
                training_mode: enq.training_mode,
                batch_time: enq.batch_time,
                branch_location: enq.branch_location,
                alternative_email: enq.alternative_email,
                alternative_mobile: enq.alternative_mobile,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
            success: function(response) {
                window.location.href = "/enquiries/list/"
                // submit();
                // alert("Enquiry added successfully");
                // document.getElementById('id01').style.display='block'
                // demo.showSwal('enquiry-success')
                // demo.showEnquiryNotification()
                // console.log(enq.id)
            },
            error: function(response) {
                demo.showSwal('enquiry-error')
            }
    });
});

function sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function success() {
  var frm = $('#new_enquiry_form').serializeArray();
  var flag = true;
  for(var i=0;i<frm.length;i++){
    if(frm[i].value === ""){
      if(frm[i].name == "alternative_email"){
        flag = true; break;
      } else if (frm[i].name == "alternative_mobile") {
        flag = true; break;
      }
       flag = false; break;
     }
   }
  if(flag === false) {
    document.getElementById('sbtbtn').disabled = true;
  }
  else{
      document.getElementById('sbtbtn').disabled = false;
    }
}

$(function () {
$('.datetime-input').datetimepicker({
    format:'YYYY-MM-DD HH:mm:ss'
  });
});

$(function () {
  $('.myCustomDateFormat').datetimepicker({
      format:'YYYY-MM-DD'
  });
});

$.fn.serializeObject = function(){
  var obj = {};
  $.each( this.serializeArray(), function(i,o){
    var n = o.name,
        v = o.value;
        obj[n] = obj[n] === undefined ? v
          : $.isArray( obj[n] ) ? obj[n].concat( v )
          : [ obj[n], v ];
  });
  return obj;
};

var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
var $table = $('#bootstrap-table');

function operateFormatter(value, row, index) {
    return [
        '<a rel="tooltip" title="View" class="btn btn-link btn-info table-action view" href="javascript:void(0)">',
        '<i class="fa fa-image"></i>',
        '</a>',
        '<a rel="tooltip" title="Edit" class="btn btn-link btn-warning table-action edit" href="javascript:void(0)">',
        '<i class="fa fa-edit"></i>',
        '</a>',
        '<a rel="tooltip" title="Remove" class="btn btn-link btn-danger table-action remove" href="javascript:void(0)">',
        '<i class="fa fa-remove"></i>',
        '</a>'
    ].join('');
}

$().ready(function() {
    window.operateEvents = {
        'click .view': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click view icon, row: ', info);
            console.log(info);
        },
        'click .edit': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click edit icon, row: ', info);
            console.log(info);
        },
        'click .remove': function(e, value, row, index) {
            console.log(row);
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
        }

    };

    $table.bootstrapTable({
        toolbar: ".toolbar",
        clickToSelect: true,
        showRefresh: true,
        search: true,
        showToggle: true,
        showColumns: true,
        pagination: true,
        searchAlign: 'left',
        pageSize: 8,
        clickToSelect: false,
        pageList: [8, 10, 25, 50, 100],

        formatShowingRows: function(pageFrom, pageTo, totalRows) {
            //do nothing here, we don't want to show the text "showing x of y from..."
        },
        formatRecordsPerPage: function(pageNumber) {
            return pageNumber + " rows visible";
        },
        icons: {
            refresh: 'fa fa-refresh',
            toggle: 'fa fa-th-list',
            columns: 'fa fa-columns',
            detailOpen: 'fa fa-plus-circle',
            detailClose: 'fa fa-minus-circle'
        }
    });

    //activate the tooltips after the data table is initialized
    $('[rel="tooltip"]').tooltip();

    $(window).resize(function() {
        $table.bootstrapTable('resetView');
    });
});


function setFormValidation(id) {
    $(id).validate({
        highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
            $(element).closest('.form-check').removeClass('has-success').addClass('has-error');
        },
        success: function(element) {
            $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
            $(element).closest('.form-check').removeClass('has-error').addClass('has-success');
        },
        errorPlacement: function(error, element) {
            $(element).closest('.form-group').append(error).addClass('has-error');
        },
    });
}

function submit() {
  /*Put all the data posting code here*/
 document.getElementById("myForm").reset();
}

function setFormValidation(id) {
    $(id).validate({
        highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
            $(element).closest('.form-check').removeClass('has-success').addClass('has-error');
        },
        success: function(element) {
            $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
            $(element).closest('.form-check').removeClass('has-error').addClass('has-success');
        },
        errorPlacement: function(error, element) {
            $(element).closest('.form-group').append(error).addClass('has-error');
        },
    });
}

$(document).ready(function() {
    setFormValidation('#AddCourses');
});

function submit() {
  /*Put all the data posting code here*/
 document.getElementById("myForm").reset();
}

function CourseAddFunction(){
  swal({
    title: 'Good job!',
    text: 'Your Course Successfully Add.',
    type: 'success',
    showCancelButton: true,
    confirmButtonClass: "btn btn-info btn-fill",
    confirmButtonText: "Okay",
    cancelButtonClass: "btn btn-danger btn-fill",
    closeOnConfirm: false,
  }, function(CourseConfirm){
    if (CourseConfirm){
      document.getElementById("AddCourses").reset();
      location.reload();
    } else {
      location.reload();
    }
  }
)
}


var $table = $('#bootstrap-table');

function operateFormatter(value, row, index) {
    return [
        '<a rel="tooltip" title="Edit" class="btn btn-link btn-warning table-action edit" href="javascript:void(0)">',
        '<i class="fa fa-edit"></i>',
        '</a>',
        '<a rel="tooltip" title="Remove" class="btn btn-link btn-danger table-action remove" href="javascript:void(0)">',
        '<i class="fa fa-remove"></i>',
        '</a>'
    ].join('');
}

$().ready(function() {
    window.operateEvents = {
     'click .edit': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click edit icon, row: ', info);
            console.log(info);
        },
        'click .remove': function(e, value, row, index) {
            console.log(row);
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
        }
    };

    $table.bootstrapTable({
        toolbar: ".toolbar",
        clickToSelect: true,
        showRefresh: true,
        search: true,
        showToggle: true,
        showColumns: true,
        pagination: true,
        searchAlign: 'right',
        pageSize: 8,
        clickToSelect: false,
        pageList: [8, 10, 25, 50, 100],

        formatShowingRows: function(pageFrom, pageTo, totalRows) {
            //do nothing here, we don't want to show the text "showing x of y from..."
        },
        formatRecordsPerPage: function(pageNumber) {
            return pageNumber + " rows visible";
        },
        icons: {
            refresh: 'fa fa-refresh',
            toggle: 'fa fa-th-list',
            columns: 'fa fa-columns',
            detailOpen: 'fa fa-plus-circle',
            detailClose: 'fa fa-minus-circle'
        }
    });

    //activate the tooltips after the data table is initialized
    $('[rel="tooltip"]').tooltip();

    $(window).resize(function() {
        $table.bootstrapTable('resetView');
    });


});

$('#exampleModal').on('show.bs.modal', function (event) {
var button = $(event.relatedTarget) // Button that triggered the modal
var recipient = button.data('whatever') // Extract info from data-* attributes
// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
var modal = $(this);
modal.find('.modal-title').text('New message to ' + recipient);
modal.find('.modal-body input').val(recipient);
$('#enrollmentid').val(email);

});

function setFormValidation(id) {
    $(id).validate({
        highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
            $(element).closest('.form-check').removeClass('has-success').addClass('has-error');
        },
        success: function(element) {
            $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
            $(element).closest('.form-check').removeClass('has-error').addClass('has-success');
        },
        errorPlacement: function(error, element) {
            $(element).closest('.form-group').append(error).addClass('has-error');
        },
    });
}

// $(function () {
//   $('input.time-input').timepicker({
//     timeFormat: 'HH:mm'
//   });
// });


/* ---Enquiry form javascript start here--- */
var email = '';

$(document).on('submit', '#new_enroll_form', function(e){
e.preventDefault();

var enrolls = $('#new_enroll_form').serializeObject();

/* ---console is used for debugging purpose at browser--- */
console.log(enrolls);
var enquiry_url = enrolls['enquiryid']

$.ajax({
        type:'POST',
        url :'/enrollments/' + enquiry_url + "/",
        data :{
            enquiryid: enrolls.enquiryid,
            discuss_fee: enrolls.discuss_fee,
            registration_amount: enrolls.registration_amount,
            payment_method: enrolls.payment_method,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(response){
          window.location.href = '/enrollments/view/' + response.id
        },
        error: function(response){
            demo.showSwal('enroll-error')
        }
      });
});

$.fn.serializeObject = function(){
var obj = {};
$.each( this.serializeArray(), function(i,o){
  var n = o.name,
      v = o.value;
      obj[n] = obj[n] === undefined ? v
        : $.isArray( obj[n] ) ? obj[n].concat( v )
        : [ obj[n], v ];
});
return obj;
};
function submit() {
/*Put all the data posting code here*/
document.getElementById("new_enquiry_form").reset();
}




// $(document).on('submit', '#installment', function(e){
//     e.preventDefault();

// var installs = $('#installment').serializeObject();

/* ---console is used for debugging purpose at browser--- */

// console.log(installs);

$('#installment_submit').click(function(e){
  e.preventDefault()
  var installs = $('#installment').serializeObject();
  $.ajax({
          type:'POST',
          url :'/enrollments/installment/',
          data :{
              installments: installs.installments,
              due_date: installs.fee_date,
              enrollmentid: installs.enrollmentid,
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
          success:function(response){
              alert("Installment added successfully");
          }
  });
});


$.fn.serializeObject = function(){
var obj = {};
$.each( this.serializeArray(), function(i,o){
  var n = o.name,
      v = o.value;
      obj[n] = obj[n] === undefined ? v
        : $.isArray( obj[n] ) ? obj[n].concat( v )
        : [ obj[n], v ];
});
return obj;
};
function submit() {
/*Put all the data posting code here*/
document.getElementById("installment").reset();
}

function results(){
	var followupMode = document.getElementById('followupMode').value;
	var response = document.getElementById('response').value;
	var nextFolloup = document.getElementById('nextFolloup').value;
	var comment = document.getElementById('comment').value;

	location.reload();
}

// {% comment %}
// $('#followup_submit').click(function(e){
//   e.preventDefault();
//   var follows = $('#followup').serializeObject();
//   console.log(follows);
//   $.ajax({
//           type:'POST',
//           url :'/enquiries/',
//           data :{
//               followups_mode: follows.followups_mode,
//               response: follows.response,
//               next_followup: follows.next_followup,
//               comment: follows.comment,
//               csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//           },
//           success:function(response){
//               alert("FollowUps added successfully");
//           }
//   });
// });
//
// function submit() {
// /*Put all the data posting code here*/
// document.getElementById("followup").reset();
// }
//
// {% endcomment %}

$.fn.serializeObject = function(){
  var obj = {};
  $.each( this.serializeArray(), function(i,o){
    var n = o.name,
        v = o.value;
        obj[n] = obj[n] === undefined ? v
          : $.isArray( obj[n] ) ? obj[n].concat( v )
          : [ obj[n], v ];
  });
  return obj;
};

var $table = $('#bootstrap-table');
$(document).ready(function() {
    // var $table = $('#bootstrap-table').bootstrapTable();
    //$table.dataTable();
    $table.bootstrapTable();
    window.operateEvents = {
        'click .view': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click view icon, row: ', info);
            console.log(info);
        },
        'click .edit': function(e, value, row, index) {
            info = JSON.stringify(row);

            swal('You click edit icon, row: ', info);
            console.log(info);
        },
        'click .remove': function(e, value, row, index) {
            console.log(row);
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
        }

    };

// $(document).on('submit', '#new_batches_form', function(e){
//     e.preventDefault();
//
//     var batches = $('#new_batches_form').serializeObject();
//
// /* ---console is used for debugging purpose at browser--- */
//
//     console.log(batches);
//     var bd = '';
//     var trainer = '';
//     var candidate = '';
//
//     for(var i = 0; i<batches.days_of_week.length; i++){
//         if(i === 0){
//         bd += batches.days_of_week[i];
//         }
//         else{
//             bd += ',' + batches.days_of_week[i];
//         }
//     }
//
//     for(var i = 0; i<batches.instructors.length; i++){
//         if(i === 0){
//         trainer += batches.instructors[i];
//         }
//         else{
//             trainer += ',' + batches.instructors[i];
//         }
//     }
//
//     for(var i = 0; i<batches.candidates.length; i++){
//         if(i === 0){
//         candidate += batches.candidates[i];
//         }
//         else{
//             candidate += ',' + batches.candidates[i];
//         }
//     }
//
//     console.log(bd);
//     console.log(trainer);
//     $.ajax({
//             type:'POST',
//             url :'/batches/',
//             data :{
//                 batch_name: batches.batch_name,
//                 days_of_week: bd,
//                 start_time: batches.start_time,
//                 end_time: batches.end_time,
//                 duration: batches.duration,
//                 start_date: batches.start_date,
//                 instructors: trainer,
//                 course_content: batches.course_content,
//                 candidate = candidate,
//                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//             },
//             success:function(){
//
//                 alert("Batches added successfully");
//             }
//     });
// });
//   $.fn.serializeObject = function(){
//     var obj = {};
//     $.each( this.serializeArray(), function(i,o){
//       var n = o.name,
//           v = o.value;
//           obj[n] = obj[n] === undefined ? v
//             : $.isArray( obj[n] ) ? obj[n].concat( v )
//             : [ obj[n], v ];
//     });
//     return obj;
//   };
function submit() {
  /*Put all the data posting code here*/
 document.getElementById("new_batches_form").reset();
}

    // $table.bootstrapTable({
    //     toolbar: ".toolbar",
    //     clickToSelect: true,
    //     showRefresh: true,
    //     search: true,
    //     showToggle: true,
    //     showColumns: true,
    //     pagination: true,
    //     searchAlign: 'left',
    //     pageSize: 8,
    //     clickToSelect: false,
    //     pageList: [8, 10, 25, 50, 100],
    //
    //     formatShowingRows: function(pageFrom, pageTo, totalRows) {
    //         //do nothing here, we don't want to show the text "showing x of y from..."
    //     },
    //     formatRecordsPerPage: function(pageNumber) {
    //         return pageNumber + " rows visible";
    //     },
    //     icons: {
    //         refresh: 'fa fa-refresh',
    //         toggle: 'fa fa-th-list',
    //         columns: 'fa fa-columns',
    //         detailOpen: 'fa fa-plus-circle',
    //         detailClose: 'fa fa-minus-circle'
    //     }
    // });

    //activate the tooltips after the data table is initialized
    $('[rel="tooltip"]').tooltip();

    $(window).resize(function() {
        // $table.bootstrapTable('resetView');
    });
});

// enquiry college and company input field javascript

function dyninput(cbox){
  if (cbox.name == "company_input"){
    if (cbox.checked == true){
      document.getElementsByName('college_input')[0].disabled = true;
      var inputCollegeOrCompany = document.getElementById('inputCollegeOrCompany');
      inputCollegeOrCompany.disabled = false
      inputCollegeOrCompany.placeholder = "Company"
    } else {
      document.getElementsByName('college_input')[0].disabled = false;
      var inputCollegeOrCompany = document.getElementById('inputCollegeOrCompany');
      inputCollegeOrCompany.disabled = true
      inputCollegeOrCompany.placeholder = ""
    }
  } else if (cbox.name == "college_input") {
    if (cbox.checked == true){
      document.getElementsByName('company_input')[0].disabled = true;
      var inputCollegeOrCompany = document.getElementById('inputCollegeOrCompany')
      inputCollegeOrCompany.disabled = false
      inputCollegeOrCompany.placeholder = "College"
    } else {
      document.getElementsByName('company_input')[0].disabled = false;
      var inputCollegeOrCompany = document.getElementById('inputCollegeOrCompany')
      inputCollegeOrCompany.disabled = true
      inputCollegeOrCompany.placeholder = ""
    }
  }
};

// $('#UnpaidButton').is('checked', function() {
//   $.ajax({
//     url: enrollpayUrl,
//     type: "GET",
//     data: $(this).serialize(),
//     success: function() {
//       window.location.href = window.location.href;
//     },
//   });
// });

function myEnrollInstFunc(EnrollPayUrl){
  swal({
    title: "Select Payment Mode",
    html: document.getElementById('DevPaymentMethod').innerHTML,
    showCancelButton: true,
    closeOnConfirm: false,
    allowOutsideClick: false
  }, function(){
    var selectPayMethod = document.getElementsByName('PaymentMethod')[1].value;
    $.ajax({
      url: EnrollPayUrl,
      type: "GET",
      data: {
        "InstallMentPaymentMethod": selectPayMethod,
      }, success: function(){
        window.location.href = window.location.href;
      }
    })
  })

    // $('#PaymentMethod').change(function(){
    //  var selectValue = $('#PaymentMethod :selected').val();
    //  alert(selectValue)
};



function OpenSendCoures(input_attr, post_url,send_type){
  swal({
    title: "Please select course to send on "+(send_type==1?'Email':'SMS'),
    html: document.getElementById('DevCoursesSend').innerHTML,
    showCancelButton: true,
    confirmButtonText: "Send",
    closeOnConfirm: false,
    allowOutsideClick: false
  }, function(){
    var all_courses = document.getElementsByName('CoursesSend')[1].value;
    $.ajax({
      url: post_url,
      type: 'POST',
      beforeSend: function(){
        $('#cover-spin').show(0);
      },
      data: {
        'courses': all_courses,
        'send_type':send_type,
      },
      success: function(r){
        if (r.status==1) {
          location.reload();
        } else {
          location.reload();
        }
      },
      complete: function(){
        $('#cover-spin').hide(0);
      }
    })
  })
}

function OpendAccountDetailsSend(input_attr, post_url,send_type){
  swal({
    title: "Share payment details on "+(send_type==1?'Email':'SMS') ,
    // html: document.getElementById('DevCoursesSend').innerHTML,
    confirmButtonText: "Send",
    showCancelButton: true,
    closeOnConfirm: false,
    allowOutsideClick: false
  }, function(){
    $.ajax({
      url: post_url,
      type: 'POST',
      data: {
        'send_type':send_type,
      },
      beforeSend: function(){
        $('#cover-spin').show(0);
      },
      success: function(r){
        if (r.status==1) {
          location.reload();
        } else {
          location.reload();
        }
      },
      complete: function(){
        $('#cover-spin').hide(0);
      }
    })
  })
}

// $.ajax({
//   url: EnrollPayUrl,
//   type: "GET",
//   data: {},
//   success: function(){
//     window.location.href = window.location.href;
//   }
// })

function enrollFunction(urlArgs){
  swal({
      title: "Are you sure to enroll the enquiry?",
      showCancelButton: true,
      confirmButtonClass: "btn btn-info btn-fill",
      confirmButtonText: "Confirm",
      cancelButtonClass: "btn btn-danger btn-fill",
      closeOnConfirm: false,
  }, function(inconfirm) {
      if (inconfirm) {
        window.location.href = urlArgs;
      }
  });
};

function EnquireCourseDataDiscard(DiscardUrl,ask_for_reason){
  reason=''
  if(ask_for_reason){
    reason=prompt('Whats the reason of discard?');
    if(!reason){
      return;
    }
  }
  swal({
    title: "Are you sure to discard this course?",
    showCancelButton: true,
    confirmButtonText: "Confirm",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function() {
      $.ajax({
        url: DiscardUrl,
        type: "POST",
        data: 'reason='+reason,
        success: function(){
          //window.location.href = window.location.href;
	  location.reload();
        }
    })
  })
}

function EnquireCourseDataUnDiscard(DiscardUrl,ask_for_reason){
  reason=''
  swal({
    title: "Are you sure to Undiscard this course?",
    showCancelButton: true,
    confirmButtonText: "Confirm",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function() {
      $.ajax({
        url: DiscardUrl,
        type: "POST",
        data: 'reason=',
        success: function(){
          //window.location.href = window.location.href;
	  location.reload();
        }
    })
  })
}
var total_submitted_fees = 0;
$('.instamt').each(function (index, element) {
  total_submitted_fees = total_submitted_fees + parseInt($(element).text());
});

var total_fees = parseInt($('input[name=discuss_fee]').val());
var total_remaining_fees = total_fees - total_submitted_fees;
$('#remaining-fees').text(total_remaining_fees);
if (total_remaining_fees == 0){
  var myEnrollModal = document.getElementById('modaldataToggle')
  myEnrollModal.dataset['target'] = ""
}

$("#installments").on('input', function(){
  var installment_amount = parseInt($("input[name=installments]").val());
  var installment_amount = isNaN(parseInt(installment_amount)) ? 0 : parseInt(installment_amount);
  var current_remaining_fees = total_remaining_fees;
  $('#remaining-fees').text(current_remaining_fees - installment_amount);
});

// $('.multi_select_fastselect').fastselect();

$("#candidateSearch").fastselect();


// $('#course_delete').on('click', function(e, post_url){
function course_delete_function(e, post_url){
  e.preventDefault();
  swal({
    title: "Are you sure to Delete this Course!",
    text: "You will not be go back!",
    type: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, Delete!",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function() {
    $.ajax({
      url: post_url,
      type: 'GET',
      async: false,
      success: function(r){
        if (r.status == 1){
          swal({
            title: 'Good job!',
            text: 'This Course Successfully deleted',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
      } else {
        swal({
          title: 'WARNING to delete',
          text: 'This Course could not be delete. (many batches are running with same course)',
          type: 'warning',
          showCancelButton: true,
          confirmButtonClass: "btn btn-info btn-fill",
          confirmButtonText: "Okay",
          cancelButtonClass: "btn btn-danger btn-fill",
          closeOnConfirm: false,
        }, function(CourseConfirm){
          if (CourseConfirm){
            location.reload();
          } else {
            location.reload();
          }
        })
      }
    }
    });
  })
}

function delete_instructor_function(e, post_url){
  e.preventDefault();
  swal({
    title: "Are you sure to Delete Instructor!",
    text: "You will not be go back!",
    type: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, Delete!",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function() {
    $.ajax({
      url: post_url,
      type: 'GET',
      async: false,
      success: function(r){
        if (r.status == 1) {
          swal({
            title: 'Good job!',
            text: 'The Instructor Successfully deleted',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        } else {
          swal({
            title: 'WARNING to delete',
            text: 'This Instructor could not be delete. (many batches are running with this instructor)',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        }
      }
    });
  })
}

$('#update_batch').on('submit', function(e){
  e.preventDefault();
  swal({
    title: "Are you sure to Update Batch!",
    text: "You will not be go back!",
    type: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, Delete!",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function(){
    var update_data = $('#update_batch').serializeArray();
    console.log(update_data);
    $.ajax({
      url: `${$('#update_batch').attr('action')}`,
      type: 'POST',
      data: update_data,
      success: function(r){
        if (r.status == 1) {
          swal({
            title: 'Good job!',
            text: 'The Batch Successfully updated',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              window.location.href=r.redirect;
            } else {
              window.location.href=r.redirect;
            }
          })
        } else {
          swal({
            title: 'WARNING to Update',
            text: 'This Batch could not be update. (Contact to Admin)',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              window.location.href=r.redirect;
            } else {
              window.location.href=r.redirect;
            }
          })
        }
      }
    });
  }
  )
});

$('#update_instructor').on('submit', function(e){
  e.preventDefault();
  var update_instructor_from_data = $(this).serializeObject();
  var update_instructor_attr_action = $(this).attr('action');
  swal({
    title: "Are you sure to Update Instructor!",
    text: "You will not be go back!",
    type: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, Update!",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function(){
    $.ajax({
      url: update_instructor_attr_action,
      type: 'POST',
      data: update_instructor_from_data,
      success: function(r){
        if (r.status==1) {
          swal({
            title: 'Good job!',
            text: 'The Instructor Successfully updated',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              window.location.href=r.redirect;
            } else {
              window.location.href=r.redirect;
            }
          })
        } else {
          swal({
            title: 'WARNING to Update',
            text: 'This Instructor could not be update. (Contact to Admin)',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              window.location.href=r.redirect;
            } else {
              window.location.href=r.redirect;
            }
          })
        }
      }
    });
  })
});

function discard_followups(e, post_url){
  var checked = $(e.target)[0].checked;
  
  e.preventDefault();
  var reason = "";
  if(checked){
    reason=prompt('Whats the reason of discard?');
  }
  var url = post_url;
  swal({
    title: "Are you sure to Discard this Followup!",
    text: "You will not be go back!",
    type: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, Discard!",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function(){
    $.ajax({
      url: url,
      type: 'POST',
      data:'reason='+reason,
      success: function(r){
        if (r.status==1) {
          swal({
            title: 'Good job!',
            text: 'The Followup Successfully Discard',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        } else {
          swal({
            title: 'WARNING to Discard',
            text: 'This Followup could not be Discard. (Contact to Admin)',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        }
      }
    });
  })
}

function discard_enquiry(e, post_url){
  e.preventDefault();
  var url = post_url;
  reason=prompt('Whats the reason of discard?');
  if(!reason){
    return;
  }
  swal({
    title: "Are you sure to discard this Enquiry?",
    showCancelButton: true,
    confirmButtonText: "Yes, Discard",
    closeOnConfirm: false,
  }, function(){
    $.ajax({
      url: url,
      type: 'POST',
      data:'reason='+reason,
      success: function(r){
        if (r.status == 1) {
          swal({
            title: 'The enquiry successfully discarded.',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        } else {
          swal({
            title: 'This enquiry could not be discarded.',
            text: 'Please contact admin.',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        }
      }
    });
  })
}

function undiscard_enquiry(e, post_url){
  e.preventDefault();
  var url = post_url;
  swal({
    title: "Are you sure to Undiscard this Enquiry?",
    showCancelButton: true,
    confirmButtonText: "Yes, Undiscard",
    closeOnConfirm: false,
  }, function(){
    $.ajax({
      url: url,
      type: 'POST',
      success: function(r){
        if (r.status == 1) {
          swal({
            title: 'The enquiry successfully undiscarded.',
            type: 'success',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        } else {
          swal({
            title: 'This enquiry could not be undiscarded.',
            text: 'Please contact admin.',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: "btn btn-info btn-fill",
            confirmButtonText: "Okay",
            cancelButtonClass: "btn btn-danger btn-fill",
            closeOnConfirm: false,
          }, function(CourseConfirm){
            if (CourseConfirm){
              location.reload();
            } else {
              location.reload();
            }
          })
        }
      }
    });
  })
}

function make_url(){
  var url = new URL(window.location.href);
  var query_string = url.search;
  var search_params = new URLSearchParams(query_string);
  search_params.set(`d`, `${$('#daysfilter option:selected').val()}`);
  url.search = search_params.toString();
  var new_url = url.toString();
  window.location.href = new_url;
}

function own_filter_url(attr_input){
  var url = new URL(window.location.href);
  var query_string = url.search;
  var search_params = new URLSearchParams(query_string);
  var select_filter = $("#ownfilter option:selected").val()
  search_params.set(`o`, `${select_filter}`);
  url.search = search_params.toString();
  var new_url = url.toString();
  window.location.href = new_url;
}

function interest_filter(attr_input){
  var url = new URL(window.location.href);
  var query_string = url.search;
  var search_params = new URLSearchParams(query_string);
  var select_filter = $("#interest_filter option:selected").val()
  search_params.set(`interest`, `${select_filter}`);
  url.search = search_params.toString();
  var new_url = url.toString();
  window.location.href = new_url;
}

function search_filter(attr_input){
  if (attr_input.keyCode == 13) {
    var url = new URL(window.location.href);
    var query_string = url.search;
    var search_params = new URLSearchParams(query_string);
    var select_filter = $("#filters option:selected").val()
    search_params.set(`type`, `${select_filter}`);
    search_params.set(`n`, `${$('#filters_search').val()}`)
    url.search = search_params.toString();
    var new_url = url.toString();
    window.location.href = new_url;
  }
}

function session_duration_check(input_attr){
  value = $(`#${input_attr.getAttribute('id')}`).val()
  if (value >= 1) {
    $(`#${input_attr.getAttribute('id')}`).val(value)
  } else {
    $(`#${input_attr.getAttribute('id')}`).val(1)
  }
}

$('#update_installment').on('submit', function(e){
  e.preventDefault();
  var form_data = $(this).serializeObject();
  swal({
    title: "Are you sure to update this Installment?",
    showCancelButton: true,
    confirmButtonText: "Yes",
    confirmButtonClass: "btn btn-info btn-fill",
    closeOnConfirm: false,
  }, function(){
      $.ajax({
        url: `${window.location.pathname}`,
        type: 'POST',
        data: form_data,
        success: function(r){
          if(r.status == 1){
            swal({
              title: 'The Installment successfully updated',
              type: 'success',
              showCancelButton: true,
              confirmButtonClass: "btn btn-info btn-fill",
              confirmButtonText: "Okay",
              cancelButtonClass: "btn btn-danger btn-fill",
              closeOnConfirm: false,
            }, function(CourseConfirm){
              if (CourseConfirm){
                window.location.href = `${r.redirect}`
              } else {
                window.location.href = `${r.redirect}`
              }
            })
          } else {
            swal({
              title: 'WARNING to Update Installment',
              text: 'This Installment could not be Update. (Contact to Admin)',
              type: 'warning',
              showCancelButton: true,
              confirmButtonClass: "btn btn-info btn-fill",
              confirmButtonText: "Okay",
              cancelButtonClass: "btn btn-danger btn-fill",
              closeOnConfirm: false,
            }, function(CourseConfirm){
              if (CourseConfirm){
                window.location.href = `${r.redirect}`
              } else {
                window.location.href = `${r.redirect}`
              }
            })
          }
        }
      });
    }
  )
});
