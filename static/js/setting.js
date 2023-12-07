// app.js
$(document).ready(function() {
    
    var index=0;
    var list=["image1.jpg","image2.jpg","image3.jpg","image4.jpg","image5.jpg","image6.jpg","image7.jpg","image8.jpg","image9.jpg","image10.jpg"
    ,"image11.jpg","image12.jpg","image13.jpg","image14.jpg","image15.jpg","image16.jpg","image17.jpg","image18.jpg","image19.jpg","image20.jpg"
    ,"image21.jpg","image22.jpg","image23.jpg","image24.jpg","image25.jpg","image26.jpg","image27.jpg","image28.jpg","image29.jpg","image30.jpg"
    ,"image31.jpg","image31.jpg","image32.jpg","image33.jpg","image34.jpg","image35.jpg"];
    
    document.getElementById('bypass').click();
    var bypassButton = document.getElementById('bypass');
    var recordingButton = document.getElementById('recording');
    var alarmButton = document.getElementById('alarm');
    var shiftButton = document.getElementById('shift');
    var versionButton = document.getElementById('version_setting');
    var cameraButton = document.getElementById('cam_setting');
    var uptimeButton =document.getElementById('uptime_setting');
    var terminalButton =document.getElementById('Terminal_setting');
    

    function colorchange_navBar(cus_nav){
        bypassButton.style.color="blue";
        recordingButton.style.color="blue";
        alarmButton.style.color="blue";
        shiftButton.style.color="blue"; 
        machineName.style.color="blue";
        machineName.style.backgroundColor="rgb(212, 219, 219)";
        uptimeButton.style.color="blue";
        uptimeButton.style.backgroundColor="rgb(212, 219, 219)";
        terminalButton.style.color="blue";
        terminalButton.style.backgroundColor="rgb(212, 219, 219)";
        cameraButton.style.color="blue";
        cameraButton.style.backgroundColor="rgb(212, 219, 219)";
        versionButton.style.color="blue";
        bypassButton.style.backgroundColor="rgb(212, 219, 219)";
        recordingButton.style.backgroundColor="rgb(212, 219, 219)";
        alarmButton.style.backgroundColor="rgb(212, 219, 219)";
        shiftButton.style.backgroundColor="rgb(212, 219, 219)";
        versionButton.style.backgroundColor="rgb(212, 219, 219)";
        uptimeButton.style.backgroundColor="rgb(212, 219, 219)";
        cus_nav.style.color="white";
        cus_nav.style.backgroundColor="blue";
    }


// Define your functions

function updateSwitchState(switchId, status) {
    const checkbox = document.getElementById(switchId);

    if (checkbox) {
        checkbox.checked = status === 1;
        checkbox.disabled = false;
    }
}

function disableSwitches(switchIds) {
    for (const switchId of switchIds) {
        const checkbox = document.getElementById(switchId);
        if (checkbox) {
            checkbox.checked = false;
            checkbox.disabled = true;
        }
    }
}

function updateStatus() {
    $.ajax({
        url: '/uptimestatus',
        method: 'GET',
        success: function (data) {
            console.log(data);

            if (Array.isArray(data) && data.length > 0) {
                const featureStatusMappings = [
                    { id: 'cameraSwitch', index: 0 },
                    { id: 'controllerSwitch', index: 1 },
                    { id: 'machineSwitch', index: 2 },
                    { id: 'softwareSwitch', index: 3 },
                    { id: 'mlSwitch', index: 4 },
                    { id: 'alarmSwitch', index: 5 },
                    { id: 'monitorSwitch', index: 6 }
                ];

                for (const { id, index } of featureStatusMappings) {
                    const status = data[0][index];
                    if (status !== undefined) {
                        updateSwitchState(id, parseInt(status, 10));
                    }
                }

                $.ajax({
                    url: '/check_server_statuses',
                    method: 'GET',
                    success: function (data) {
                        const mlStatus = data[0] === '1' ? 1 : 0;
                        const alarmmsStatus = data[1] === '1' ? 1 : 0;
                        const monitorStatus = data[2] === '1' ? 1 : 0;
                        updateSwitchState('mlSwitch', mlStatus);
                        updateSwitchState('alarmSwitch', alarmmsStatus);
                        updateSwitchState('monitorSwitch', monitorStatus);

                        for (let i = 0; i < data.length; i++) {
                            console.log(`${i} is ${data[i]}`);
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("AJAX request failed:", status, error);
                        disableSwitches(['mlSwitch', 'alarmSwitch', 'monitorSwitch']);
                    }
                });
            } else {
                console.error("Unexpected data format:", data);
                disableSwitches(['cameraSwitch', 'controllerSwitch', 'machineSwitch', 'softwareSwitch', 'mlSwitch', 'alarmSwitch', 'monitorSwitch']);
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX request failed:", status, error);
            disableSwitches(['cameraSwitch', 'controllerSwitch', 'machineSwitch', 'softwareSwitch', 'mlSwitch', 'alarmSwitch', 'monitorSwitch']);
        }
    });
}

// Declare and initialize the flag for continuous status updates
let uptimeStatusUpdate = {
    Status: true,
    IntervalId: null
};
function startContinuousStatusUpdate() {
    console.log("Attempting to start continuous status updates...");

    if (!uptimeStatusUpdate.Status) {
        console.log("Continuous status updates have been stopped.");
        return;
    }

    try {
        intervalId = setInterval(() => {
            try {
                updateStatus();
            } catch (error) {
                console.error("An error occurred while updating status: " + error.message);
                clearInterval(intervalId);
                uptimeStatusUpdate.Status = false;
            }
        }, 1000);
    } catch (error) {
        console.error("An error occurred during the continuous update setup: " + error.message);
        clearInterval(intervalId);
        uptimeStatusUpdate.Status = false;
    }
}

// Event listener for the 'uptimeButton' click
uptimeButton.addEventListener('click', function () {
    colorchange_navBar(uptimeButton);

    clearInterval(intervalId);

    startContinuousStatusUpdate();

  
    
    var uptime_html = `
    
    <table>
    
        <tbody>
            <tr>
            <th style="font-size: 30px;">HARDWARE</th>
            <th style="font-size: 30px;">STATUS</th>
            </tr>

            <tr>
                <td style="font-size: 35px;">Camera</td>
    
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="cameraSwitch" name="cameraStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                  
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Controller &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="controllerSwitch" name="controllerStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Sensor</td>
                
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="machineSwitch" name="machineStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Core</td>
               
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="softwareSwitch" name="softwareStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Ml</td>
              
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="mlSwitch" name="mlStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Alarm</td>
              
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="alarmSwitch" name="alarmmsStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <tr>
                <td style="font-size: 35px;">Monitor</td>
               
                <td>
                    <label class="switch1">
                        <input type="checkbox" id="monitorSwitch" name="monitorStatus" disabled>
                        <div class="slider1"></div>
                    </label>
                </td>
            </tr>
            <!-- Add more rows for other features if needed -->
        </tbody>
    </table>
`;


    // Update the content in the '#newstting_data' element
    $("#newstting_data").html(uptime_html);
});

    

    // while initial loading
    var bypass_html = `<form id="bypass_form" class="form-container"  action="/updatebypass" method="post" >          
    <div>
        <table>
        <tr>
            <td><h2 style="padding-top: -10px;"for="new_fullbypass">Full Bypass:&nbsp;&nbsp; </h2></td>
            <td><label class="switch"><input id="full_bypass" name="full_bypass" type="checkbox"/><div class="slider"></div></label> </td>
        </tr>
        <tr>
            <td><h2 style="padding-top: -10px;"for="new_fullbypass">Alarm Bypass:&nbsp;&nbsp; </h2></td>
            <td><label class="switch"><input id="alarm_bypass" name="alarm_bypass" type="checkbox"/><div class="slider"></div></label> </td>
        </tr>
        <tr>
            <td><h2 style="padding-top: -10px;"for="new_fullbypass">Sensor Bypass:&nbsp;&nbsp; </h2></td>
            <td><label class="switch"><input id="sensor_bypass" name="sensor_bypass" type="checkbox"/><div class="slider"></div></label> </td>
        </tr>
        </table>       
        <button style="width:300px;" type="submit" id="new_setting_byepass" class="btn btn-primary" action="/tt">Submit</button>
    </div> 
    </form>  `     
    $("#newstting_data").html(bypass_html);
    // data from sql
    $.ajax({
        url: '/getbypass_status', // Replace with your API endpoint
        method: 'GET', // or 'POST' as needed
        success: function (data) {
            document.getElementById("full_bypass").checked = data.full_bypass;
            document.getElementById("alarm_bypass").checked = data.alarm_bypass;
            document.getElementById("sensor_bypass").checked = data.sensor_bypass;
        }
    });
    $("#bypass_form").submit(function (e) {
        e.preventDefault();
       
        var formData = $(this).serialize();
      
        $.ajax({
            url: '/updateMachineName', 
            method: 'post',
            data: formData
            
        });
    });
    
        var bypassSubmit = document.getElementById('new_setting_byepass');
        bypassSubmit.addEventListener('click', function () {  
            swal("Updated!", "Your bypass has been updated!", "success")
    }); 
    // Machine Name - event
    machineName.addEventListener('click', function () {  
        colorchange_navBar(machineName);
        clearInterval(intervalId);    
        var MachineName = `
        <form id="machineName_form" class="form-container"  action="/updateMachineName" method="post">          
        <div>
          <table>
            <tr>
              <td><h2 style="padding-top: -10px;"for="new_machineName">Machine Name:&nbsp;&nbsp; </h2></td>
              <td><label ><input id="new_machineName" name="new_machineName" type="text"/><div ></div></label> </td>
            </tr>
          </table>       
          <button style="width:300px;" type="submit" id="new_setting_machineName" class="btn btn-primary" action="/tt">Submit</button>
        </div> 
      </form>  
      `     
        $("#newstting_data").html(MachineName);
 
        $.ajax({
            url: '/get_machineName', 
            method: 'GET', 
            success: function (data) {
                document.getElementById("new_machineName").value = data.machineName;
            }
        });

    $("#machineName_form").submit(function (e) {
        e.preventDefault();
       
        var formData = $(this).serialize();
      
        $.ajax({
            url: '/updateMachineName', 
            method: 'post',
            data: formData
            
        });
    });
        var machineNameSubmit = document.getElementById('new_setting_machineName');
        machineNameSubmit.addEventListener('click', function () {  
            swal("Updated!", "Your machine name has been updated!", "success")
    }); 
    });

    // version
    versionButton.addEventListener('click', function () {  
        colorchange_navBar(versionButton);
        clearInterval(intervalId);    
        var version_html = `
        <form id="machineName_form" class="form-container"  action="/updateMachineName" method="post">          
        <div>
            <table >
                <tr>
                    <th></th>
                    <th style="text-align:center">Version</th>
                    <th style="text-align:center" >Time Stamp</th>
                </tr>
                <tbody style="input[type=text]{padding: 12px 50px;}">
                <tr>
                    <td><h2 style="padding-top: -10px;"for="new_machineName">Core Version:&nbsp;&nbsp; </h2></td>
                    <td><label ><input style="text-align:center" id="core_version" name="core_version" type="text"/><div ></div></label> </td>
                    <td><label ><input style="text-align:center" id="core_version_ts" name="core_version_ts" type="text"/><div ></div></label> </td>
                </tr>
                <tr>
                    <td><h2 style="padding-top: -10px;"for="new_machineName">Alarm Version:&nbsp;&nbsp; </h2></td>
                    <td><label ><input style="text-align:center" id="alarm_version" name="alarm_version" type="text"/><div ></div></label> </td>
                    <td><label ><input style="text-align:center" id="alarm_version_ts" name="alarm_version_ts" type="text"/><div ></div></label> </td>
                </tr>
                <tr>
                    <td><h2 style="padding-top: -10px;"for="new_machineName">Report Version:&nbsp;&nbsp; </h2></td>
                    <td><label ><input style="text-align:center" id="report_version" name="report_version" type="text"/><div ></div></label> </td>
                    <td><label ><input style="text-align:center" id="report_version_ts" name="report_version_ts" type="text"/><div ></div></label> </td>
                </tr>
                <tr>
                    <td><h2 style="padding-top: -10px;"for="new_machineName">Monitor Version:&nbsp;&nbsp; </h2></td>
                    <td><label ><input style="text-align:center" id="monitor_version" name="monitor_version" type="text"/><div ></div></label> </td>
                    <td><label ><input style="text-align:center" id="monitor_version_ts" name="monitor_version_ts" type="text"/><div ></div></label> </td>
                </tr>
                <tr>
                    <td><h2 style="padding-top: -10px;"for="new_machineName">Webui Version:&nbsp;&nbsp; </h2></td>
                    <td><label ><input style="text-align:center" id="webui_version" name="webui_version" type="text"/><div ></div></label> </td>
                    <td><label ><input style="text-align:center" id="webui_version_ts" name="webui_version_ts" type="text"/><div ></div></label> </td>
                </tr>
                </tbody>
          </table>       
        </div> 
      </form>  
      `     
        $("#newstting_data").html(version_html);
        // data from sql
        $.ajax({
            url: '/get_version', // Replace with your API endpoint
            method: 'GET', // or 'POST' as needed
            success: function (data) {
                document.getElementById("core_version").value = data.core_version;
                document.getElementById("core_version_ts").value = data.core_version_ts;
                document.getElementById("alarm_version").value = data.alarm_version;
                document.getElementById("alarm_version_ts").value = data.alarm_version_ts;
                document.getElementById("report_version").value = data.report_version;
                document.getElementById("report_version_ts").value = data.report_version_ts;
                document.getElementById("monitor_version").value = data.monitor_version;
                document.getElementById("monitor_version_ts").value = data.monitor_version_ts;
                document.getElementById("webui_version").value = data.webui_version;
                document.getElementById("webui_version_ts").value = data.webui_version_ts;
                
                document.getElementById("core_version").readOnly=true;
                document.getElementById("core_version").style.border='none';
                document.getElementById("core_version").style.outline='none';

                document.getElementById("core_version_ts").readOnly=true;
                document.getElementById("core_version_ts").style.border='none';
                document.getElementById("core_version_ts").style.outline='none';

                document.getElementById("alarm_version").readOnly=true;
                document.getElementById("alarm_version").style.border='none';
                document.getElementById("alarm_version").style.outline='none';

                document.getElementById("alarm_version_ts").readOnly=true;
                document.getElementById("alarm_version_ts").style.border='none';
                document.getElementById("alarm_version_ts").style.outline='none';

                document.getElementById("report_version").readOnly=true;
                document.getElementById("report_version").style.border='none';
                document.getElementById("report_version").style.outline='none';

                document.getElementById("report_version_ts").readOnly=true;
                document.getElementById("report_version_ts").style.border='none';
                document.getElementById("report_version_ts").style.outline='none';

                document.getElementById("monitor_version").readOnly=true;
                document.getElementById("monitor_version").style.border='none';
                document.getElementById("monitor_version").style.outline='none';

                document.getElementById("monitor_version_ts").readOnly=true;
                document.getElementById("monitor_version_ts").style.border='none';
                document.getElementById("monitor_version_ts").style.outline='none';

                document.getElementById("webui_version").readOnly=true;
                document.getElementById("webui_version").style.border='none';
                document.getElementById("webui_version").style.outline='none';

                document.getElementById("webui_version_ts").readOnly=true;
                document.getElementById("webui_version_ts").style.border='none';
                document.getElementById("webui_version_ts").style.outline='none';

            }
        });
        var machineNameSubmit = document.getElementById('new_setting_machineName');
        
    });

    // terminalButton
    terminalButton.addEventListener('click', function () {  
        colorchange_navBar(terminalButton);
        clearInterval(intervalId);    
        var Terminal_html = `
            <h1>
                CountAi - Terminal    
            </h1>
        
            <iframe src="https://localhost:8500"
                    height="500px" width="1000px">
            </iframe>
      `     
        $("#newstting_data").html(Terminal_html);
        
    });


    // bypass - event
    bypassButton.addEventListener('click', function () {  
        colorchange_navBar(bypassButton);
        clearInterval(intervalId);    
        var bypass_html = `
        <form id="bypass_form" class="form-container"  action="/updatebypass" method="post">          
        <div>
          <table>
            <tr>
              <td><h2 style="padding-top: -10px;"for="new_fullbypass">Full Bypass:&nbsp;&nbsp; </h2></td>
              <td><label class="switch"><input id="full_bypass" name="full_bypass" type="checkbox"/><div class="slider"></div></label> </td>
            </tr>
            <tr>
              <td><h2 style="padding-top: -10px;"for="new_fullbypass">Alarm Bypass:&nbsp;&nbsp; </h2></td>
              <td><label class="switch"><input id="alarm_bypass" name="alarm_bypass" type="checkbox"/><div class="slider"></div></label> </td>
            </tr>
            <tr>
              <td><h2 style="padding-top: -10px;"for="new_fullbypass">Sensor Bypass:&nbsp;&nbsp; </h2></td>
              <td><label class="switch"><input id="sensor_bypass" name="sensor_bypass" type="checkbox"/><div class="slider"></div></label> </td>
            </tr>
          </table>       
          <button style="width:300px;" type="submit" id="new_setting_byepass" class="btn btn-primary" action="/tt">Submit</button>
        </div> 
      </form>  
      `     
        $("#newstting_data").html(bypass_html);
        // data from sql
        $.ajax({
            url: '/getbypass_status', // Replace with your API endpoint
            method: 'GET', // or 'POST' as needed
            success: function (data) {
                document.getElementById("full_bypass").checked = data.full_bypass;
                document.getElementById("alarm_bypass").checked = data.alarm_bypass;
                document.getElementById("sensor_bypass").checked = data.sensor_bypass;
            }
        });
        
        var bupassSubmit = document.getElementById('new_setting_byepass');
        bupassSubmit.addEventListener('click', function () {  
        swal("Updated!", "Your Bypass settings has been updated!", "success")
    }); 
    });
    // recording menu
    
    recordingButton.addEventListener('click', function () {       
        colorchange_navBar(recordingButton);
      var recording_html = `
      <div class="container justify-content-center" style="margin-left: 40px;margin-right: 10px;">
        <div class="row ">          
          <div class="col-9" id="livecam">
            <img style="width: 100%;height: 100%;" id="livecamera" src="../static/images/Knit_i.jpeg" alt="">
          </div>
          <div class="col-3">
            
            <div class="row" style="width: 700px;">

                 <form id="recording_form" class="form-container" action="/updaterecording" method="post" >          
                    <div>
                        <table>
                        <tr>
                            <td><h4 style="padding-top: -10px;">Live Camera:&nbsp;&nbsp; </h4></td>
                            <td><label class="switch"><input onchange="enableSaveimg()" id="bypass_livecamera" name="bypass_livecamera" type="checkbox"/><div class="slider"></div></label> </td>
                        </tr>
                        <tr>
                            <td><h4 style="padding-top: -10px;">Save Image:&nbsp;&nbsp; </h4></td>
                            <td><label class="switch"><input id="bypass_saveimg" name="bypass_saveimg" disabled type="checkbox"/><div class="slider"></div></label> </td>
                        </tr>
                        <tr>
                            <td><h5 style="padding-top: -10px;">Folder Name:&nbsp;&nbsp; </h5></td>
                            <td><input id="bypass_imgpath" name="bypass_imgpath" type="text" disabled/></td>               
                        </tr>
                        <tr>
                            <td><h5 style="padding-top: -10px;">Camera FPS:&nbsp;&nbsp; </h5></td>
                            <td><input id="bypass_fps"  name="bypass_fps" type="number" min="1" max="20" step="1"  value="1" disabled/></td>
                        </tr>
                        </table> 
                        <div class="text-center">
                            <button style="width:300px;" type="submit" id="new_setting_saveimg" class="btn btn-primary text-center">Submit</button>
                        </div>      
                    </div>
                </form>   
            </div>
            <br>

            <div class="row">
                <div id="slider-container">
                    <div id="image-slider">
                        <img style="width: 700px; height: 300px;"  id="image-slide" class="slider-image" src="../static/images/ref_img/image1.jpg" alt="Image 1">
                    </div>
                </div>
                <div class="d-flex justify-content-between ">
                    <div class="p-2 bd-highlight">
                        <button style="width: 300px;" id="pre-button">Previous</button>
                    </div>
                    <div class="p-2 bd-highlight">
                        <button style="width: 300px;" id="next-button">Next</button>
                    </div>
                </div>         
            </div>
          </div>
        </div>
      </div>  
      `
        $("#newstting_data").html(recording_html);
        clearInterval(intervalId);   
        var live_cam_checkbox = document.getElementById('bypass_livecamera')
        var save_img_checkbox = document.getElementById('bypass_saveimg')
        var img_path = document.getElementById('bypass_imgpath')
        var img_fps = document.getElementById('bypass_fps')
        
        live_cam_checkbox.addEventListener('change', function () {
            if (live_cam_checkbox.checked) {
                startContinuousLoading();
                save_img_checkbox.disabled = false;
                img_path.disabled = false;
                img_fps.disabled = false;
            } else {
                save_img_checkbox.checked = false;
                save_img_checkbox.disabled = true;
                img_path.disabled = true;
                img_fps.disabled = true;
                shouldContinue = false;
                clearInterval(intervalId);   
            }
        });

            const slider1 = document.getElementById("image-slide");
            const prevButton = document.getElementById("pre-button");
            const nextButton = document.getElementById("next-button");

            
            prevButton.addEventListener("click", () => {
                slider1.src="../static/images/ref_img/"+list[Math.abs((--index) %35)];
            });
            nextButton.addEventListener("click", () => {
                slider1.src="../static/images/ref_img/"+list[Math.abs((++index) %35)];
            });
            document.getElementById("image-slider").addEventListener("click",function(){
                var recording_html2=`
                <div class="col-12" style="padding-left:80%;">
                <button type="button" class="btn-close" id="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="container justify-content-center">
                <img style="width: 100%; height: 550px;" id="image-slide1" class="slider-image" src="../static/images/ref_img/image1.jpg" alt="Image 1">
                    <div class="d-flex justify-content-between ">
                        <div class="p-2 bd-highlight">
                            <button style="width: 300px;" id="pre-button1">Previous</button>
                        </div>
                        <div class="p-2 bd-highlight">
                            <button style="width: 300px;" id="next-button1">Next</button>
                        </div>
                    </div>
                </div>
                `
                $("#newstting_data").html(recording_html2);
                document.getElementById("btn-close").addEventListener("click",function(){
                    recordingButton.click();
                });
                const slider2=document.getElementById("image-slide1");
                document.getElementById("pre-button1").addEventListener("click", () => {
                    slider2.src="../static/images/ref_img/"+list[Math.abs((--index) %35)];
                });
                document.getElementById("next-button1").addEventListener("click", () => {
                    slider2.src="../static/images/ref_img/"+list[Math.abs((++index) %35)];
                });
            });
    
            document.getElementById("livecam").addEventListener("click",function(){
                clearInterval(intervalId);   

                var recording_html3=`
                <div class="col-12" style="padding-left:80%;">
                <button type="button" class="btn-close" id="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="container justify-content-center">
                    <img style="width: 100%;height: 635px;" id="livecamera" src="../static/images/Knit_i.jpeg" alt="">
                </div>
                `
                startContinuousLoading();

                $("#newstting_data").html(recording_html3);
                document.getElementById("btn-close").addEventListener("click",function(){
                    recordingButton.click();
                });
            });


        var saveIMGSubmit = document.getElementById('new_setting_saveimg');
        // startContinuousLoading();
        // function enableSaveimg(){

        //     if(live_cam_checkbox.checked){
        //         save_img_checkbox.disabled = false;
        //         img_path.disabled = false;
        //         img_fps.disabled = false;                
        //     }else{
        //         save_img_checkbox.disabled = true;
        //         img_path.disabled = true;
        //         img_fps.disabled = true;
        //     }/home/santhosh/NPS/KnittingUI-Demo/python_file/shift.py
        // }
        // data getting from db for recording
        $.ajax({
            url: '/get_recording', // Replace with your API endpoint
            method: 'GET', // or 'POST' as needed
            success: function (data) {
                document.getElementById("bypass_livecamera").checked = data.livecamera_status;
                document.getElementById("bypass_saveimg").checked = data.saveimage_status;
                document.getElementById("bypass_imgpath").value = data.image_path;
                document.getElementById("bypass_fps").value = data.fps;
                console.log(data.livecamera_status)

                if (data.livecamera_status) {
                    console.log("checked",live_cam_checkbox.value)
                    startContinuousLoading();
                    save_img_checkbox.disabled = false;
                    img_path.disabled = false;
                    img_fps.disabled = false;
                }
            }

            
        });
        $("#recording_form").submit(function (e) {
            e.preventDefault(); // Prevent the default form submission behavior
            // Collect form data
            var formData = $(this).serialize();
            // Send the form data using AJAX
            $.ajax({
                url: '/updaterecording', // Replace with your endpoint
                method: 'post',
                data: formData
                
            });
        });
        saveIMGSubmit.addEventListener('click', function () {
            const bypass_fps = document.getElementById("bypass_fps").value 
            if($("#bypass_fps").attr('checked', true)){
                console.log("true")
                if (bypass_fps <= 20 & bypass_fps >= 1  ){
                    clearInterval(intervalId);
                    swal("Updated!", "Your Recording settings has been updated!", "success")
                }else{
                    swal("Invalid FPS!", "Please check your FPS!", "error")
    
                }
            }
            swal("Updated!", "Your Recording settings has been updated!", "success")
        }); 

    });
    
    // DOFF FORM
    // var errorModal = new bootstrap.Modal(document.getElementById('errorModal')); // Initialize the error modal
    // var exampleModal = new bootstrap.Modal(document.getElementById('exampleModal')); // Initialize the example modal

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

    // show continue modal-old
    document.addEventListener('DOMContentLoaded', function() {
        const myModal = document.getElementById('myModal');
        const myInput = document.getElementById('myInput');
    
        myModal.addEventListener('shown.bs.modal', () => {
            myInput.focus();
        });
    });

    // var imgElementdfectcenter = document.getElementById('image');
            
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
            data = null;
              console.log('updateDefectDetails success');
              setTimeout(updateDefectDetails, updateInterval);
          }
      });
    }


    
    
    
   

    // setting -alarm
    function get_alarm_setting() {
        console.log('get_alarm_setting')
        $.ajax({
            url: '/get_alarm_setting',
            method: 'GET',
            success: function(data) {
                console.log(data)
                createTable1(data);
              console.log('get_alarm_setting success');
              data = null;
            //   setTimeout(get_alarm_setting, 3000);
            }
        });
    }
     
    function createTable1(data) {
        const table = document.createElement('table');
        // Create table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow();

        const headings = ['Deftect Id', 'Defect Name', 'Alarm Status', 'Instance Count', 'Sensitivity'];

        headings.forEach(heading => {
        const th = document.createElement('th');
        th.textContent = heading;
        th.style.width='150px';
        headerRow.appendChild(th);
        });
    
        // Create table rows and cells
        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            
            for (const key in item) {
                const cell = row.insertCell();
                if (key === 'score') {
                    // Create an input element for the "score" column
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.min = 0;
                    input.max = 100;
                    input.step = 1;
                    input.value = item[key]*100; // Set the initial value from the data
                    input.id = 'scoreInput' + item['adefecTypeId']; 
                    input.name = 'scoreInput' + item['adefecTypeId']; 
                    cell.appendChild(input);
                } else if(key === 'minimumAlarmCount'){
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.min = 0;
                    input.max = 10;
                    input.step = 1;
                    input.value = item[key]; // Set the initial value from the data
                    console.log('minimumAlarmCountInput' + item['adefecTypeId']);
                    cell.appendChild(input);
                    input.id = 'minimumAlarmCountInput' + item['adefecTypeId']; // Use a unique ID for each input element
                    input.name = 'minimumAlarmCountInput' + item['adefecTypeId']; 
                }else if(key === 'alarmStatus'){
                    const switchLabel = document.createElement('label');
                    switchLabel.classList.add('switch');
                    const switchInput = document.createElement('input');
                    switchInput.type = 'checkbox';
                    switchInput.checked = item[key] === '1' ? true : false// Set the initial checked state item[key] === 1; 
                    switchInput.id = 'alarmStatusInput' + item['adefecTypeId'];
                    switchInput.name = 'alarmStatusInput' + item['adefecTypeId'];
                    const switchSlider = document.createElement('div');
                    switchSlider.classList.add('slider');
                    switchLabel.appendChild(switchInput);
                    switchLabel.appendChild(switchSlider);
                    cell.appendChild(switchLabel);
                }else if(key === 'adefecTypeId'){   
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'adefecTypeId' + item['adefecTypeId']; 
                    input.name = 'adefecTypeId' + item['adefecTypeId']; 
                    input.readOnly=true;
                    input.style.border='none';
                    input.style.outline='none'; 
                    cell.appendChild(input);
                }else if(key === 'adefectName'){   
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'adefectName' + item['adefecTypeId']; 
                    input.name = 'adefectName' + item['adefecTypeId']; 
                    input.style.border='none';
                    input.style.outline='none';
                    input.readOnly=true;
                    cell.appendChild(input);
                }
                else {
                    cell.textContent = item[key];
                }                               
            }
            
        });
    
        // Append the table to the container
        const tableContainer = document.getElementById('table-container1');
        tableContainer.innerHTML = ''; // Clear previous content
        tableContainer.appendChild(table);
    }

    
    alarmButton.addEventListener('click', function () { 
        colorchange_navBar(alarmButton);
        clearInterval(intervalId);    
        var alarm_html = `
        <form id="recording_form" class="form-container"  action="/updatealarmsetting" method="post">          
        <div>
            <div id="newstting_data">
                <table>
                    <tbody id="table-container1">
                        <!-- Table content generated using JavaScript -->
                        <!-- You can add your dynamic content here -->
                    </tbody>
                </table>     
                    <button style="width:300px;" type="submit" id="new_setting_alarm" class="btn btn-primary">Submit</button>
        </div>
        </form>
      `     
      $("#newstting_data").html(alarm_html);
      get_alarm_setting();
      var new_setting_alarm = document.getElementById('new_setting_alarm');
      new_setting_alarm.addEventListener('click', function (e) {
      e.preventDefault(); 
     
      $.ajax({
          url: '/updatealarmsetting',
          method: 'POST',
          data: $('form#recording_form').serialize(), 
          success: function (data) {
           
              swal("Updated!", data.message, "success");
          }
      });
  });
});
    
    // camera-setting
    function get_camera_setting() {
        $.ajax({
            url: '/get_camera_setting',
            method: 'GET',
            success: function(data) {
                settingCameraTable(data);
                data = null;
            }
        });
    }
     
    function settingCameraTable(data) {
        const table = document.createElement('table');
        // Create table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow();

        const headings = ['Camera Id', 'Camera Name', 'Camera Status'];

        headings.forEach(heading => {
        const th = document.createElement('th');
        th.textContent = heading;
        th.style.width='150px';
        headerRow.appendChild(th);
        });
    
        // Create table rows and cells
        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            
            for (const key in item) {
                const cell = row.insertCell();

                if(key === 'camsts_id'){
                    const switchLabel = document.createElement('label');
                    switchLabel.classList.add('switch');
                    const switchInput = document.createElement('input');
                    switchInput.type = 'checkbox';
                    switchInput.checked = item[key] === 1 ? true : false// Set the initial checked state item[key] === 1; 
                    switchInput.id = 'cameraStatusInput' + item['cam_id'];
                    switchInput.name = 'cameraStatusInput' + item['cam_id'];
                    const switchSlider = document.createElement('div');
                    switchSlider.classList.add('slider');
                    switchLabel.appendChild(switchInput);
                    switchLabel.appendChild(switchSlider);
                    cell.appendChild(switchLabel);
                }else if(key === 'cam_id'){   
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'cameraId' + item['cam_id']; 
                    input.name = 'cameraId' + item['cam_id']; 
                    input.readOnly=true;
                    input.style.border='none';
                    input.style.outline='none'; 
                    cell.appendChild(input);
                }else if(key === 'cam_name'){   
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'cameraName' + item['cam_id']; 
                    input.name = 'cameraName' + item['cam_id']; 
                    input.style.border='none';
                    input.style.outline='none';
                    // input.readOnly=true;
                    cell.appendChild(input);
                }
                else {
                    cell.textContent = item[key];
                }                               
            }
            
        });
    
        // Append the table to the container
        const tableContainer = document.getElementById('table-container3');
        tableContainer.innerHTML = ''; // Clear previous content
        tableContainer.appendChild(table);
    }

    
    cameraButton.addEventListener('click', function () { 
        colorchange_navBar(cameraButton);
        clearInterval(intervalId);    
        var camera_html = `
        <form id="camera_form" class="form-container"  action="/updatecamera" method="post">          
        <div>
            <div id="newstting_data">
                <table>
                    <tbody id="table-container3">
                        <!-- Table content generated using JavaScript -->
                        <!-- You can add your dynamic content here -->
                    </tbody>
                </table>     
                    <button style="width:300px;" type="submit" id="new_setting_camera" class="btn btn-primary">Submit</button>
        </div>
        </form>
      `     
        $("#newstting_data").html(camera_html);
        get_camera_setting();
        $("#camera_form").submit(function (e) {
            e.preventDefault(); // Prevent the default form submission behavior
            // Collect form data
            var formData = $(this).serialize();
            // Send the form data using AJAX
            $.ajax({
                url: '/updatecamera', // Replace with your endpoint
                method: 'post',
                data: formData
                
            });
        });
        var new_setting_camera = document.getElementById('new_setting_camera');
        new_setting_camera.addEventListener('click', function () {  
            swal("Updated!", "Your Camera settings has been updated!", "success")
            
        }); 
    });
    

    // shift - setting
    shiftButton.addEventListener('click', function () { 
        colorchange_navBar(shiftButton);
        clearInterval(intervalId);    
        var alarm_html = `
        <form id="shift_form" class="form-container"  action="/updateshiftsetting" method="post">          
        <div>
            <div id="newstting_data">
                <table>
                    <tbody id="table-container2" style="input[type=text]{padding: 12px 50px;}">
                        <!-- Table content generated using JavaScript -->
                        <!-- You can add your dynamic content here -->
                    </tbody>
                </table>     
                    <button style="width:300px;" type="submit" id="new_setting_shift" class="btn btn-primary">Submit</button>
        </div>
        </form>
      `     
        $("#newstting_data").html(alarm_html);
        get_shift_setting();
        var new_setting_shift = document.getElementById('new_setting_shift');
        new_setting_shift.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent the form from submitting
            // Send an AJAX request to the /updateshiftsetting route
            $.ajax({
                url: '/updateshiftsetting',
                method: 'POST',
                data: $('form#shift_form').serialize(), // Serialize the form data
                success: function (data) {
                    // Handle the success response (data.message) and display a message
                    swal("Updated!", data.message, "success");
                }
            });
        });

        // var new_setting_shift = document.getElementById('new_setting_shift');
        // new_setting_shift.addEventListener('click', function () {  
        //     swal("Updated!", "Your Alarm settings has been updated!", "success")
            
        // }); 


        document.getElementById('shift_form').addEventListener('submit', function (event) {
            // Prevent the default form submission
            event.preventDefault();
        
            // Call your data verification function
            if (verifyData()) {
              // If data is valid, manually submit the form
                this.submit();
                swal("Updated!", "Your Shift Time has been updated!", "success")

            } else {
              // Handle invalid data (e.g., display an error message)
            //   alert('Invalid data. Please check your input.');
              swal("Alart!", "Please Enter valid Shift Time!", "warning")

            }
          });
        
          function verifyData() {
            // Implement your data verification logic here
            // Return true if data is valid, false otherwise
            //var a = document.getElementById('start_time1').value;
            var a = document.getElementById('start_time1').value;
            var b = document.getElementById('end_time1').value;
            var c = document.getElementById('start_time2').value;
            var d = document.getElementById('end_time2').value;
            var e = document.getElementById('start_time3').value;
            var f = document.getElementById('end_time3').value;
            var result = false; 
             
            const timeRanges = [
                { start: a, end: b},
                { start: c, end: d },
                { start: e, end: f }
              ];
              
              const isValidTime = (time) => {
                const [hour, minute] = time.split(":").map(Number);
                return hour >= 0 && hour < 24 && minute >= 0 && minute < 60;
              };
              
              const totalDurationMinutes = timeRanges.reduce((total, { start, end }) => {
                if (isValidTime(start) && isValidTime(end)) {
                  const [startHour, startMinute] = start.split(":").map(Number);
                  const [endHour, endMinute] = end.split(":").map(Number);
                  let durationMinutes = (endHour * 60 + endMinute) - (startHour * 60 + startMinute);
                  if (durationMinutes < 0) {
                    durationMinutes += 24 * 60;
                  }
                  return total + durationMinutes;
                } else {
                  return -1;
                }
              }, 0);
              
              if (totalDurationMinutes === 1440) {
                console.log("24 hours");
                result = true;
              } else if (totalDurationMinutes === -1) {
                console.log("Input time is wrong");
                result = false;
              } else {
                console.log("Shift times are incorrect");
                result = false;
              }             
            a = null;
            b = null;
            c = null;
            d = null;
            e = null;
            f = null;
            return result
            }
        
    });

    function get_shift_setting() {
        console.log('get_shift_setting')
        $.ajax({
            url: '/get_shift_setting',
            method: 'GET',
            success: function(data) {
                console.log(data)
                createTable2(data);
              console.log('get_shift_setting success');
              data = null;
            //   setTimeout(get_alarm_setting, 3000);
            }
        });
    }


    function createTable2(data) {
        const table = document.createElement('table');
        // Create table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow();

        const headings = ['Shift ID', 'Shift Name', 'Start Tme', 'End Time'];

        headings.forEach(heading => {
        const th = document.createElement('th');
        th.textContent = heading;
        th.style.width='150px';
        headerRow.appendChild(th);
        });
    
        // Create table rows and cells
        const tbody = table.createTBody();
        data.forEach(item => {
            const row = tbody.insertRow();
            
            for (const key in item) {
                const cell = row.insertCell();
                if (key === 'ashift_id') {
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'shift_id' + item['ashift_id']; 
                    input.name = 'shift_id' + item['ashift_id']; 
                    input.readOnly=true;
                    input.style.border='none';
                    input.style.outline='none'; 
                    input.style.padding = '5px';
                    cell.appendChild(input);
                    
                } else if(key === 'bshift_name'){
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'shift_name' + item['ashift_id']; 
                    input.name = 'shift_name' + item['ashift_id']; 
                    input.readOnly=false;
                    input.style.border='none';
                    input.style.outline='none'; 
                    cell.appendChild(input);
                    
                }else if(key === 'cstart_time'){
                    const input = document.createElement('input');
                    input.type = 'time';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'start_time' + item['ashift_id']; 
                    input.name = 'start_time' + item['ashift_id']; 
                    input.readOnly=false;
                    // input.style.border='none';
                    // input.style.outline='none'; 
                    cell.appendChild(input);
                    
                }else if(key === 'dend_time'){   
                    const input = document.createElement('input');
                    input.type = 'time';
                    input.value = item[key] // Set the initial value from the data
                    input.id = 'end_time' + item['ashift_id']; 
                    input.name = 'end_time' + item['ashift_id']; 
                    input.readOnly=false;
                    // input.style.border='none';
                    // input.style.outline='none'; 
                    cell.appendChild(input);
                }
                else {
                    cell.textContent = item[key];
                }                               
            }
            
        });
    
        // Append the table to the container
        const tableContainer = document.getElementById('table-container2');
        tableContainer.innerHTML = ''; // Clear previous content
        tableContainer.appendChild(table);
    }

             

    
    
    
    // Function to initiate image loading based on the toggle state
    function loadImage() {
        var live_cam_checkbox = document.getElementById('bypass_livecamera')

        // console.log(live_cam_checkbox)
        try{
            if(live_cam_checkbox.checked == true){
                try{
                    var imgElementlivecam = document.getElementById('livecamera'); 
                    const url = '/update_image';          
                    $.ajax({
                        url: url,
                        method: 'GET',
                        success: function (data) {
                            imgElementlivecam.src = data; 
                            data=null;              
                            console.log(`Success - Update Image from ${url}`);
                        }
                    });
                }catch(error){
                    console.log('error');
                    return;
                }
            }else{
                imgElementlivecam.src = "../static/images/Knit_i.jpeg";               
            }
        }catch{
            try{
                var imgElementlivecam = document.getElementById('livecamera'); 
                    const url = '/update_image';          
                    $.ajax({
                        url: url,
                        method: 'GET',
                        success: function (data) {
                            imgElementlivecam.src = data; 
                            data=null;              
                            console.log(`Success - Update Image from ${url}`);
                        }
                    });
            }catch(error){
                console.log('error');
                return;
            }
        }
        
        
    }
    
    let intervalId;
    let shouldContinue = true;

    function startContinuousLoading() {
        if (!shouldContinue) {
            console.log("Continuous loading has been stopped.");
            return;
        }

        try {
            intervalId = setInterval(() => {
                try {
                    loadImage();
                } catch (error) {
                    console.error("An error occurred while loading the image: " + error.message);
                    clearInterval(intervalId); // Stop the continuous loading
                    shouldContinue = false; // Set the flag to stop further execution
                }
            }, 100); // Set the update interval time in milliseconds
        } catch (error) {
            console.error("An error occurred during the continuous loading setup: " + error.message);
            clearInterval(intervalId); // Stop the continuous loading
            shouldContinue = false; // Set the flag to stop further execution
        }
    }

    // To stop the continuous loading at any time:
    function stopContinuousLoading() {
        clearInterval(intervalId);
        shouldContinue = false;
        console.log("Continuous loading has been manually stopped.");
    }

    
    


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
});
