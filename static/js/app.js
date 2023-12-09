// app.js
$(document).ready(function() {

    document.body.addEventListener("touchstart", function(event) {
        if (event.touches.length === 3) {
            $(document).ready(function() {
                $('#myModal').modal('show');
                document.getElementById('passwordForm').addEventListener('submit', function(event) {
                  event.preventDefault();
                  const passwordInput = document.getElementById('password');
                  const password = passwordInput.value;
              
                  if (password === '123') {
                    window.location.replace("setting");
                  } 
                  // Close the modal
                  $('#myModal').modal('hide');
                });
              });
            //window.location.replace("setting");
        }
    });

    document.getElementById("submit").addEventListener("click",function(){
        Swal.fire({
            title: 'Are you sure?',
            text: 'You won\'t be able to revert this!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, save and submit it!",
            cancelButtonText: "No, only submit it!",
          }).then((result) => {
            if (result.isConfirmed) {
                var form = document.getElementById('settings-form'); 
                var formData = new FormData(form); 
                $.ajax({ 
                    url: '/settingsUpdate1', 
                    method: 'POST', 
                    data: formData, 
                    processData: false, 
                    contentType: false, 
                }); 
            } 
            else
            {
                var form = document.getElementById('settings-form'); 
                var formData = new FormData(form); 
                $.ajax({ 
                    url: '/settingsUpdate', 
                    method: 'POST', 
                    data: formData, 
                    processData: false, 
                    contentType: false, 
                }); 
            }
          });
        // swal({
        //     title: "Are you sure?",
        //     text: "New roll will be started!",
        //     type: "warning",
        //     showCancelButton: true,
        //     confirmButtonColor: "#DD6B55",
        //     confirmButtonText: "Yes, save and submit it!",
        //     cancelButtonText: "No, only submit it!",
        //     closeOnConfirm: false,
        //     closeOnCancel: false
        //   },
        //   function(isConfirm){
        //     if (isConfirm) {
              
        //         $.ajax({
        //             url: '/startNewRollUpdate', // Replace with your API endpoint
        //             method: 'GET', // or 'POST' as needed
        //             success: function () {
        //                 console.log("startNewRollUpdate has been Done!");                
        //             },
        //             error: function (error) {
        //                 console.error('Error:', error);
        //             }
        //         });
        //         swal("Success!", "Your new roll has been started.", "success");
        //     } 
        //     else {
        //         swal("Cancelled", "New Roll Will not started :)", "error");
        //     }
        //   });
    });

   document.getElementById("Saved_program_1").addEventListener("click", function(){
    $.ajax({
        url: '/get_saved_program_1', // Replace with your API endpoint
        method: 'GET', // or 'POST' as needed
        success: function (data) {
            
        }
    });
   });


    document.body.addEventListener("keydown", function (event) {
        if (event.key === "Escape"){
            $(document).ready(function() {
                $('#myModal').modal('show');
                
                document.getElementById('passwordForm').addEventListener('submit', function(event) {
                  event.preventDefault();
                  const passwordInput = document.getElementById('password');
                  const password = passwordInput.value;
              
                  if (password === '123') {
                    window.location.replace("setting");

                  } else {
                    document.body.style.visibility = 'hidden';
                    alert("Sorry your password is wrong");
                  }
              
                  // Close the modal
                  $('#myModal').modal('hide');
                });
              });
        }
    });
    // DOFF FORM
    var errorModal = new bootstrap.Modal(document.getElementById('errorModal')); // Initialize the error modal
    var exampleModal = new bootstrap.Modal(document.getElementById('exampleModal')); // Initialize the example modal
    // document.getElementById('newsetting').style.color='white';

    // Listen for form submission
    $("#check").click(function () {
    var password = $('input[name="psw"]').val();
    if (password === '123') {
        errorModal.hide(); // Close the error modal
        exampleModal.show(); // Show the example modal when the password is correct
    } else {
        $('#errorMessage').text('Wrong Password');
        errorModal.show(); // Show the error modal when the password is incorrect
    }
    });
    var settingloginModal = new bootstrap.Modal(document.getElementById('settingloginModal')); // Initialize the error modal

    // setting login form submission
    $("#check_setting").click(function () {
        var password = $('input[name="psw_setting"]').val();
        if (password === '456') {
            settingloginModal.hide(); // Close the error modal
            var a = document.getElementById('newsetting'); //or grab it by tagname etc
            a.href = "setting"
            document.getElementById('newsetting').click();
        } else {
            $('#errorMessage_setting').text('Wrong Password');
            settingloginModal.show(); // Show the error modal when the password is incorrect
        }
        });

    // show continue modal-old
    document.addEventListener('DOMContentLoaded', function() {
        const myModal = document.getElementById('myModal');
        const myInput = document.getElementById('myInput');
    
        myModal.addEventListener('shown.bs.modal', () => {
            myInput.focus();
        });
    });

    // var imgElementdfectcenter = document.getElementById('image');
    var imgElementlivecam = document.getElementById('livecamera');          
    // var imgElementlc = document.getElementById('imagelc');
    // var imgElementld = document.getElementById('latestdectimage');  
    var rollNumber = document.getElementById('rollnumber');
    var rotation = document.getElementById('rotation');
    var machineNumber = document.getElementById('machineNumber');
    var machinestatus = document.getElementById('machinestatus');
    var topbar_doffno = document.getElementById('doff_number_r');

       
    var updateInterval = 1000;  // 1 second
    // moreinfo
    $("#moreinfo").click(function () {
        // Make an AJAX request when the button is clicked
        $.ajax({
            url: '/getmoreInfo', // Replace with your API endpoint
            method: 'GET', // or 'POST' as needed
            success: function (data) {
                var machineprgdtl_id = data.machineprgdtl_id
                var program_name = data.program_name
                var description = data.description
                var gsm_ll = data.gsm_ll
                var gg = data.gg
                var fabric_type = data.fabric_type
                var job_no = data.job_no
                var needle_drop = data.needle_drop
                var roll_weight = data.roll_weight
                var doff = data.doff
                var count = data.count
                var mill = data.mill
                var dia = data.dia
                var lot = data.lot
                var party = data.party
                var timestamp = data.timestamp
                console.log(machineprgdtl_id)                
                console.log(program_name)                
                console.log(description)
                console.log(gsm_ll)
                console.log(gg)
                console.log(fabric_type)
                console.log(job_no)
                console.log(needle_drop)
                console.log(roll_weight)
                console.log(doff)
                console.log(count)
                console.log(mill)
                console.log(dia)
                console.log(lot)
                console.log(party)
                
                // timestamp the response data
                $('#machineprgdtl_id').text(machineprgdtl_id)
                $('#program_name').text(program_name)
                $('#description').text(description)
                $('#gsm_ll').text(gsm_ll)
                $('#gg').text(gg)
                $('#fabric_type').text(fabric_type)
                $('#job_no').text(job_no)
                $('#needle_drop').text(needle_drop)
                $('#roll_weight').text(roll_weight)
                $('#doff').text(doff)
                $('#count').text(count)
                $('#mill').text(mill)
                $('#dia').text(dia)
                $('#lot').text(lot)
                $('#party').text(party)
                $('#timestamp').text(timestamp)
                data = null;
                
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    // update defect details
    function updateDefectDetails() {
      console.log('updateDefectDetails')
      $.ajax({
          url: '/update_defectDetails',
          method: 'GET',
          success: function(data) {
              
              var defectname = data.defectname;
              var rollname = data.rollname;
              var captureAt = data.captureAt;            
              console.log('defectname '+defectname)
              console.log('rollname '+rollname)
              console.log('captureAt '+captureAt)
              
              // Assign values to HTML elements
              $('#defectname').text(defectname);
              $('#rollname').text(rollname);
              $('#captureAt').text(captureAt);

              console.log('updateDefectDetails success');
              data = null; 
              setTimeout(updateDefectDetails, updateInterval);
          }
      });
  }



   
    // updateMachineDetails
    function updateMachineDetails() {
      console.log('updateMachineDetails')
      $.ajax({
          url: '/update_machineDetails',
          method: 'GET',
          success: function(data) {
              
              var machinename = data.machinename;
              var machinestatus = data.machinestatus;
              var machinedtl_name = data.machinedtl_name;
              console.log('machinename '+machinename)
              console.log('machinestatus '+machinestatus)
              // Assign values to HTML elements
              $('#machinedtl_name').text(machinedtl_name);
              
                if (machinestatus == '1') 
                    $("#machinestatus").html("<p id='machinestatus' style='color: green;' class='card-text crdtitlelm'>Running</p> ");
                else if (machinestatus == '2') 
                    $("#machinestatus").html("<p id='machinestatus' style='color: red;' class='card-text crdtitlelm'>Not Running</p> ");
                else
                    $("#machinestatus").html("<p id='machinestatus' style='color: red;' class='card-text crdtitlelm'>Maintainance</p> ");                  
              console.log('updateMachineDetails success');
              data = null; 
              setTimeout(updateMachineDetails, updateInterval);
          }
      });
     }

     // updateAlarmDetails
    const animationElement = document.getElementById('animation-element');
    const alarm_reset_button = document.getElementById('alarm_reset_button');
    let alram_button = true;
    function updateAlarmDetails() {
        console.log('updateAlarmDetails')
        $.ajax({
            url: '/getAlarmStatus',
            method: 'GET',
            success: function(data) {   
                var alarmStatus = data.status;             
                if (alarmStatus == '1') 
                    {   
                    animationElement.classList.add('card-animation');
                    alarm_reset_button.disabled = false;
                }
                else {
                    // Remove the CSS class to stop the animation
                    animationElement.classList.remove('card-animation');
                    alarm_reset_button.disabled = true;

                }    
                alram_button =alarm_reset_button.disabled            
                console.log( alram_button+'------------------------------------------')
                console.log('updateAlarmDetails success');
                data = null; 
                setTimeout(updateAlarmDetails, updateInterval);
            }
        });
       }

       console.log( !alram_button+'out------------------------------------------')
    
    // left menu clicking event
    // Add a click event listener to the clickableDiv element
    document.getElementById('ProgramclickableDiv').addEventListener('click', function () {
        // Simulate a click event on the settingsLink button
        document.getElementById('settingsLink').click();
        getting_data_program_info();
    });
    document.getElementById('reportclickableDiv').addEventListener('click', function () {
        // Simulate a click event on the reportLink button
        document.getElementById('reportLink').click();
    });
    document.getElementById('DefectLogclickableDiv').addEventListener('click', function () {
        window.location.replace('DefectLogPage');
    });
    // document.getElementById('newsettingclickableDiv').addEventListener('click', function () {
    //     document.getElementById('newsetting_h5').click();
        
    // });
    document.getElementById('DoffclickableDiv').addEventListener('click', function () {
        // Simulate a click event on the settingsLink button
        document.getElementById('Doff_b').click();
    });
    document.getElementById('MoreclickableDiv').addEventListener('click', function () {
        // Simulate a click event on the settingsLink button
        document.getElementById('moreinfo').click();
    });
    document.getElementById('NewRollclickableDiv').addEventListener('click', function () {
        // Simulate a click event on the settingsLink button
        document.getElementById('startNewRoll_button').click();
    });
    document.getElementById('animation-element').addEventListener('click', function () {
        // Simulate a click event on the settingsLink button
        document.getElementById('alarm_reset_button').click();
    });
    document.getElementById('togclickableDiv').addEventListener('click', function () {
        toggle = !toggle;
        startContinuousLoading();
        toggle ? window.location.replace('/'):null;
    });

    // roll complete feed back
    document.getElementById('rollcomplete').addEventListener('click', function () {
        swal("Updated!", "Your doff has been updated!", "success")
    });
    

    // navbar highlighting
    document.getElementById('ProgramclickableDiv').addEventListener('click', () => {     
        $('#settingModal').on('shown.bs.modal', function () {
          document.getElementById('homebutton').style.color='white';
          document.getElementById('settingsLink').style.color='black';
        });
        $('#settingModal').on('hidden.bs.modal', function () {
          document.getElementById('homebutton').style.color='black';
          document.getElementById('settingsLink').style.color='white';
        });
    });
    document.getElementById('MoreclickableDiv').addEventListener('click', () => { 
        $('#exampleModal1').on('shown.bs.modal', function () {
          document.getElementById('homebutton').style.color='white';
          document.getElementById('moreinfo').style.color='black';
        });
        $('#exampleModal1').on('hidden.bs.modal', function () {
          document.getElementById('homebutton').style.color='black';
          document.getElementById('moreinfo').style.color='white';
        });
    });
    document.getElementById('DoffclickableDiv').addEventListener('click', () => { 
        $('#errorModal').on('shown.bs.modal', function () {
          document.getElementById('homebutton').style.color='white';
          document.getElementById('Doff_b').style.color='black';
        });
        $('#errorModal').on('hidden.bs.modal', function () {
            document.getElementById('homebutton').style.color='black';
            document.getElementById('Doff_b').style.color='white';
          });
          $('#exampleModal').on('shown.bs.modal', function () {
            document.getElementById('homebutton').style.color='white';
            document.getElementById('Doff_b').style.color='black';
          });
        $('#exampleModal').on('hidden.bs.modal', function () {
          document.getElementById('homebutton').style.color='black';
          document.getElementById('Doff_b').style.color='white';
        });
    });

    document.getElementById('reportclickableDiv').addEventListener('click', () => { 
        $('#reportModal').on('shown.bs.modal', function () {
          document.getElementById('homebutton').style.color='white';
          document.getElementById('reportLink').style.color='black';
        });
        $('#reportModal').on('hidden.bs.modal', function () {
          document.getElementById('homebutton').style.color='black';
          document.getElementById('reportLink').style.color='white';
        });
    });
    // document.getElementById('newsettingclickableDiv').addEventListener('click', () => { 
    //     $('#settingloginModal').on('shown.bs.modal', function () {
    //       document.getElementById('homebutton').style.color='white';
    //       document.getElementById('newsetting').style.color='black';
    //     });
    //     $('#settingloginModal').on('hidden.bs.modal', function () {
    //       document.getElementById('homebutton').style.color='black';
    //       document.getElementById('newsetting').style.color='white';
    //     });
    // });
    // Function to continuously load images when the page loads
    function getting_data_program_info() {
        $.ajax({
            url: '/getmoreInfo_edit_programInfo', // Replace with your API endpoint
            method: 'GET', // or 'POST' as needed
            success: function (data) {
                console.log("printing data of info :"+data.mill)
                var machineprgdtl_id = data.machineprgdtl_id
                var program_name = data.program_name
                var description = data.description
                var gsm_ll = data.gsm_ll
                var gg = data.gg
                var fabric_type = data.fabric_type
                var job_no = data.job_no
                var needle_drop = data.needle_drop
                var roll_weight = data.roll_weight
                var doff = data.doff
                var count = data.count
                var mill = data.mill
                var dia = data.dia
                var lot = data.lot
                var party = data.party
                var timestamp = data.timestamp
                var machineprogram_sts_id = data.machineprogram_sts_id
                var loop_length = data.loop_length
                var knit_type = data.knit_type
                var denier = data.denier
                
                
                // timestamp the response data
                document.getElementById("rollweight_").value = data.roll_weight;
                document.getElementById("job_number").value = data.job_no;
                document.getElementById("machineno_").value = data.machineprgdtl_id;
                document.getElementById("count_").value = data.count;
                document.getElementById("lot_").value = data.lot;
                document.getElementById("needledrop_").value = data.needle_drop;
                document.getElementById("dia_").value = data.dia;
                document.getElementById("gg_").value = data.gg;
                document.getElementById("mill_").value = data.mill;
                document.getElementById("machinetype_").value = data.machine_type;
                document.getElementById("party_").value = data.party;
                document.getElementById("denier_").value = data.denier;
                document.getElementById("fabric_").value = data.fabric_type;
                document.getElementById("knittype_").value = data.knit_type;
                document.getElementById("gsm_").value = data.gsm_;
                document.getElementById("ll_").value = data.loop_length;
                document.getElementById("rotations_").value = data.doff;

                
                data = null;
                
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    }

    // live image and defect img loader
    let toggle = true; // Initially set to true
    let intervalId; // To store the interval ID
    // let xhrQueue = [];
    const scanningdiv = document.getElementById("scanningdiv");
    const icon4 = document.getElementById("vector-icon4");
    const icon5 = document.getElementById("vector-icon5");
    const icon6 = document.getElementById("vector-icon6");
    const icon7 = document.getElementById("vector-icon7");

    // Function to initiate image loading based on the toggle state
    function loadImage() {
        const url = toggle ? '/update_image' : '/update_defectimage';
        const imgTag = toggle ? "Live Camera" : 'Previous Defect';
        const imgTag1 = toggle ?  'Previous Defect' :"Live Camera" ;
        const sliderClassName = toggle ? 'ocrloader' : 'ocrloa';
        const show_braket = toggle ? 'block' : 'none';

        // const xhr = 
        $.ajax({
            url: url,
            method: 'GET',
            success: function (data) {
                imgElementlivecam.src = data;
                $('#imgTag').text(imgTag);
                $('#moreinfo_img').text(imgTag1); 
                scanningdiv.className = sliderClassName;
                icon4.style.display = show_braket
                icon5.style.display = show_braket
                icon6.style.display = show_braket
                icon7.style.display = show_braket
                data = null;               
                console.log(`Success - Update Image from ${url}`);
            }
        });

        // Add the new request to the queue
        // xhrQueue.push(xhr);
    }
    
    // Function to continuously load images when the page loads
    function startContinuousLoading() {
        loadImage(); // Initial call
        intervalId = setInterval(loadImage, 4000); // Set the update interval time in milliseconds
        // Abort all pending requests in the queue
        // for (const xhr of xhrQueue) {
        //     if (xhr.readyState !== 4) {
        //         xhr.abort();
        //     }
        // }
    }
    
    startContinuousLoading();
    
    // Toggle between URLs when the button is clicked
    // const btn = document.getElementById('moreinfo_img');   
    // const btn = document.getElementById('resetbutton');
    // btn.addEventListener('click', function onClick() {
    //     toggle = !toggle;
    // });
    
    
    
    // Alarm Rest button function
    
    $("#alarm_reset_button").click(function () {

        swal({
            title: "Are you sure?",
            type: "warning",
            showConfirmButton:!alram_button,
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, reset it!",
            cancelButtonText: "No, cancel it!",
            closeOnConfirm: false,
            closeOnCancel: false
          },
          function(isConfirm){
            if (isConfirm) {              
                // Make an AJAX request when the button is clicked
                $.ajax({
                    url: '/updateAlarmstatus', // Replace with your API endpoint
                    method: 'GET', // or 'POST' as needed
                    success: function () {
                        console.log("Alarm has been Rested!");                
                    },
                    error: function (error) {
                        console.error('Error:', error);
                    }
                });
                swal("Success!", "Your new Alarm has been rested.", "success");
            } else {
                swal("Cancelled", "Alarm reset Cancelled :)", "error");
            }
          });
        
    });

     // defectdata function
     function getdefectData() {
        console.log('getdefectData')
        $.ajax({
            url: '/getdefect_data',
            method: 'GET',
            success: function(data) {
                console.log(data)
                createTable(data);
                data = null;
                console.log('getdefectData success');
              setTimeout(getdefectData, 3000);
            }
        });
    }
     
    function createTable(data) {
        const table = document.createElement('table');
        // Create table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow();
        // for (const key in data[0]) {
        //     const th = document.createElement('th');
        //     th.textContent = key;
        //     headerRow.appendChild(th);
        // }
    
        // Create table rows and cells
        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            for (const key in item) {
                const cell = row.insertCell();
                cell.textContent = item[key];
            }
        });
    
        // Append the table to the container
        const tableContainer = document.getElementById('table-container');
        tableContainer.innerHTML = ''; // Clear previous content
        tableContainer.appendChild(table);
    }
   
    // defectdata function
    function get_defectype() {
        console.log('get_defectype')
        $.ajax({
            url: '/get_defectype',
            method: 'GET',
            success: function(data) {
                console.log(data)
                createTable1(data);
                data = null;
                console.log('getdefectData success');
              setTimeout(getdefectData, 3000);
            }
        });
    }
     
    function createTable1(data) {
        const table = document.createElement('table');
        // Create table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow();
        // for (const key in data[0]) {
        //     const th = document.createElement('th');
        //     th.textContent = key;
        //     headerRow.appendChild(th);
        // }
    
        // Create table rows and cells
        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            for (const key in item) {
                const cell = row.insertCell();
                cell.textContent = item[key];
            }
        });
    
        // Append the table to the container
        const tableContainer = document.getElementById('table-container1');
        tableContainer.innerHTML = ''; // Clear previous content
        tableContainer.appendChild(table);
    }

    $("#startNewRoll_button").click(function () {

        swal({
            title: "Are you sure?",
            text: "New roll will be started!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, start it!",
            cancelButtonText: "No, cancel it!",
            closeOnConfirm: false,
            closeOnCancel: false
          },
          function(isConfirm){
            if (isConfirm) {
              
                $.ajax({
                    url: '/startNewRollUpdate', // Replace with your API endpoint
                    method: 'GET', // or 'POST' as needed
                    success: function () {
                        console.log("startNewRollUpdate has been Done!");                
                    },
                    error: function (error) {
                        console.error('Error:', error);
                    }
                });
                swal("Success!", "Your new roll has been started.", "success");
            } else {
                swal("Cancelled", "New Roll Will not started :)", "error");
            }
          });
        // Make an AJAX request when the button is clicked
    });


    var doffupdatedModal = new bootstrap.Modal(document.getElementById('doffupdatedModal')); // Initialize the error modal
    var exampleModal = new bootstrap.Modal(document.getElementById('exampleModal')); // Initialize the example modal

    function validateForm() {
        // Get form elements by their IDs
        var doffInput = document.getElementById('doff_');
        var orderInput = document.getElementById('order');
        var rollInput = document.getElementById('roll');
        var shiftdetInput = document.querySelector('input[name="shiftdet"]:checked');

        // Check if any of the required fields are empty
        if (doffInput.value === '' || orderInput.value === '' || rollInput.value === '' || shiftdetInput === null) {
            alert('Please fill out all required fields.');
            return false; // Prevent form submission
        }
        exampleModal.hide();
        doffupdatedModal.show()

        // If form validation is successful, trigger the modal manually
        $('#doffupdatedModal').modal('show');
        return false; // Prevent form submission (we'll submit it manually)
    }


    // // setting page
    // var bypassButton = document.getElementById('bypass');
    // bypassButton.addEventListener('click', function () {       
    //     var bypass_html = `<form id="bypass_form" class="form-container"  action="/updatebypass" method="post">          
    //     <div>
    //       <table>
    //         <tr>
    //           <td><h2 style="padding-top: -10px;"for="new_fullbypass">Full Bypass:&nbsp;&nbsp; </h2></td>
    //           <td><label class="switch"><input id="full_bypass" name="full_bypass" type="checkbox"/><div class="slider"></div></label> </td>
    //         </tr>
    //         <tr>
    //           <td><h2 style="padding-top: -10px;"for="new_fullbypass">Alarm Bypass:&nbsp;&nbsp; </h2></td>
    //           <td><label class="switch"><input id="alarm_bypass" name="alarm_bypass" type="checkbox"/><div class="slider"></div></label> </td>
    //         </tr>
    //         <tr>
    //           <td><h2 style="padding-top: -10px;"for="new_fullbypass">Sensor Bypass:&nbsp;&nbsp; </h2></td>
    //           <td><label class="switch"><input id="sensor_bypass" name="sensor_bypass" type="checkbox"/><div class="slider"></div></label> </td>
    //         </tr>
    //       </table>       
    //       <button type="Submit" id="new_setting_byepass" class="btn btn-primary" action="/tt">Submit</button>
    //     </div> 
    //   </form>  `     
    //     $("#newstting_data").html(bypass_html);
    //     // data from sql
    //     $.ajax({
    //         url: '/getbypass_status', // Replace with your API endpoint
    //         method: 'GET', // or 'POST' as needed
    //         success: function (data) {
    //             document.getElementById("full_bypass").checked = data.full_bypass;
    //             document.getElementById("alarm_bypass").checked = data.alarm_bypass;
    //             document.getElementById("sensor_bypass").checked = data.sensor_bypass;
    //         }
    //     });
    // });
    // var recordingButton = document.getElementById('recording');
    // recordingButton.addEventListener('click', function () {       
    //     var recording_html = `<div>
    //     <table>
    //       <tr>
    //         <td><h4 style="padding-top: -10px;">Live Camera:&nbsp;&nbsp; </h4></td>
    //         <td><label class="switch"><input id="bypass_livecamera" type="checkbox"/><div class="slider"></div></label> </td>
    //       </tr>
    //       <tr>
    //         <td><h4 style="padding-top: -10px;">Save Image:&nbsp;&nbsp; </h4></td>
    //         <td><label class="switch"><input id="bypass_saveimg" type="checkbox"/><div class="slider"></div></label> </td>
    //       </tr>
    //       <tr>
    //         <td><h5 style="padding-top: -10px;">Image Path:&nbsp;&nbsp; </h5></td>
    //         <td><input id="bypass_imgpath" type="text" /></td>
    //       </tr>
    //       <tr>
    //         <td><h5 style="padding-top: -10px;">Camera FPS:&nbsp;&nbsp; </h5></td>
    //         <td><input id="bypass_fps" type="number" min="0" max="20" step="1"  value="0"/></td>
    //       </tr>
    //     </table>       
    //     <button type="button" id="new_setting_saveimg" class="btn btn-primary">Submit</button>
    //   </div>`     
    //     $("#newstting_data").html(recording_html);
    // });
    // var alarmButton = document.getElementById('alarm');
    // alarmButton.addEventListener('click', function () {  
    //     var alarm_html = `<div>
    //     <div id="table-container1">
                                  
    //         <table>
    //             <!-- Table content generated using JavaScript -->
    //             <!-- You can add your dynamic content here -->
    //         </table>
                                  
    //                           </div>       
    //     <button type="button" id="new_setting_byepass" class="btn btn-primary">Submit</button>
    //   </div>`     
    //     $("#newstting_data").html(alarm_html);
    //     get_defectype();
    // });
    


    // Report function
    // Get the button element
    var generateReportButton = document.getElementById('generateReportButton');
    var generateshiftA_ReportButton = document.getElementById('generateshiftA_ReportButton');
    var generateshiftB_ReportButton = document.getElementById('generateshiftB_ReportButton');
    var generateshiftC_ReportButton = document.getElementById('generateshiftC_ReportButton');
    var reportModal = new bootstrap.Modal(document.getElementById('reportModal')); // Initialize the error modal   

    // Add a click event listener to the button
    generateReportButton.addEventListener('click', function () {
        // Get the selected date from the input element
        var rdate = document.getElementById('datepicker').value;

        if (rdate ===""){
            console.log('Selected date: Empty', rdate);
            swal({
                title: "alert!",
                text: "Please Enter the date.",
                type: "warning",
                timer: 2000
              });

        }else{
            console.log('Selected date: ', rdate);
            reportModal.hide();
            $.ajax({
                url: '/report/'+rdate, // Replace with your API endpoint
                method: 'POST', // or 'POST' as needed
                success: function (data) {
                    console.log("startNewRollUpdate has been Done!");  
                    var data  = data.status
                    console.log('*************',data,'************')
                    if(data==true){
                        swal("Good job!", "Your Report has been Generated!", "success")
                        data = null;
                        setTimeout(function() {
                            window.location.replace('pdfViewer');
                          }, 2000);
                    }else{
                        swal("Alert!", "No data found!", "error")
                    }
                    
                },
                error: function (error) {
                    console.error('Error:', error);
                    swal({
                        title: "alert!",
                        text: "Not able to generate Report (check date).",
                        type: "warning",
                        timer: 2000
                      });
                }
            });
        }
    });

    generateshiftA_ReportButton.addEventListener('click', function () {
        // Get the selected date from the input element
        var rdate = document.getElementById('datepicker').value;

        if (rdate ===""){
            console.log('Selected date: Empty', rdate);
            swal({
                title: "alert!",
                text: "Please Enter the date.",
                type: "warning",
                timer: 2000
              });

        }else{
            console.log('Selected date: ', rdate);
            reportModal.hide();
            $.ajax({
                url: '/reportA/'+rdate, // Replace with your API endpoint
                method: 'POST', // or 'POST' as needed
                success: function (data) {
                    console.log("startNewRollUpdate has been Done!");  
                    var data  = data.status
                    console.log('*************',data,'************')
                    if(data==true){
                        data = null;
                        swal("Good job!", "Your Report has been Generated!", "success")
                        data = null;
                        setTimeout(function() {
                            window.location.replace('pdfViewer');
                          }, 2000);
                    }else{
                        swal("Alert!", "No data found!", "error")
                    }
                    
                },
                error: function (error) {
                    console.error('Error:', error);
                    swal({
                        title: "alert!",
                        text: "Not able to generate Report (check date).",
                        timer: 2000
                      });
                }
            });
        }
    });

    generateshiftB_ReportButton.addEventListener('click', function () {
        // Get the selected date from the input element
        var rdate = document.getElementById('datepicker').value;

        if (rdate ===""){
            console.log('Selected date: Empty', rdate);
            swal({
                title: "alert!",
                text: "Please Enter the date.",
                type: "warning",
                timer: 2000
              });

        }else{
            console.log('Selected date: ', rdate);
            reportModal.hide();
            $.ajax({
                url: '/reportB/'+rdate, // Replace with your API endpoint
                method: 'POST', // or 'POST' as needed
                success: function (data) {
                    console.log("startNewRollUpdate has been Done!");  
                    var data  = data.status
                    console.log('*************',data,'************')
                    if(data==true){
                        swal("Good job!", "Your Report has been Generated!", "success")
                        data = null;
                        setTimeout(function() {
                            window.location.replace('pdfViewer');
                          }, 2000);
                    }else{
                        swal("Alert!", "No data found!", "error")
                    }
                    
                },
                error: function (error) {
                    console.error('Error:', error);
                    swal({
                        title: "alert!",
                        text: "Not able to generate Report (check date).",
                        timer: 2000
                      });
                }
            });
        }
    });

    generateshiftC_ReportButton.addEventListener('click', function () {
        // Get the selected date from the input element
        var rdate = document.getElementById('datepicker').value;

        if (rdate ===""){
            console.log('Selected date: Empty', rdate);
            swal({
                title: "alert!",
                text: "Please Enter the date.",
                type: "warning",
                timer: 2000
              });

        }else{
            console.log('Selected date: ', rdate);
            reportModal.hide();
            $.ajax({
                url: '/reportC/'+rdate, // Replace with your API endpoint
                method: 'POST', // or 'POST' as needed
                success: function (data) {
                    console.log("startNewRollUpdate has been Done!");  
                    var data  = data.status
                    console.log('*************',data,'************')
                    if(data==true){
                        swal("Good job!", "Your Report has been Generated!", "success")
                        data = null;
                        setTimeout(function() {
                            window.location.replace('pdfViewer');
                          }, 2000);
                    }else{
                        swal("Alert!", "No data found!", "error")
                    }
                    
                },
                error: function (error) {
                    console.error('Error:', error);
                    swal({
                        title: "alert!",
                        text: "Not able to generate Report (check date).",
                        timer: 2000
                      });
                }
            });
        }
    });
    
    // updateRoation
    function updateRotation() {
      console.log('updateRotation')
      $.ajax({
          url: '/update_rotation',
          method: 'GET',
          success: function(data) {
              
            var rotationId = data.rollId;
            var rollId = data.rotationValue;
            var fabric_type = data.fabric_type;
            var doff = data.doff;
            console.log('rotationId '+rotationId)
            console.log('rollId '+rollId)
            // Assign values to HTML elements
            $('#rollnumber').text(rotationId);
            $('#rotation').text(rollId);
            $('#Fab_type').text(fabric_type);
            $('#doff_number_r').text(doff);
            console.log('Rotation success');
            data = null;
            setTimeout(updateRotation, updateInterval);
          }
      });
  }
//   calling function in loop
    
    updateRotation();
    updateMachineDetails();
    updateDefectDetails();
    updateAlarmDetails();
    getdefectData();
});
