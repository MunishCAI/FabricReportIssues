$(document).ready(function() {
    const RollNumber = document.getElementById("defectLogRollId")
    $.ajax({
        url: '/get_min_max_rollnumber', // Replace with your API endpoint
        method: 'GET', // or 'POST' as needed
        success: function (data) {
            
            RollNumber.style.border='none';
            RollNumber.style.outline='none';

            // for drop down
            var container = document.getElementById("dropdown-container");
            var selectElement = document.createElement("select");
            selectElement.setAttribute("name", "select_roll_number");
            selectElement.setAttribute("id", "select_roll_number");

            var optionElement = document.createElement("option");
            optionElement.value = "Number";
            optionElement.text = 'Choose Roll Number';
            selectElement.appendChild(optionElement);

            for (var i = data.min_rollnumber; i <= data.max_rollnumber; i++) {
                var optionElement = document.createElement("option");
                optionElement.value = i;
                optionElement.text = i;
                selectElement.appendChild(optionElement);
              }

            container.appendChild(selectElement);

            selectElement.addEventListener('change', function () {
                // Get the selected date from the input element
                // var rdate = document.getElementById('cars').value;
                slideImg.src = null;
                slideImg.src = '../static/images/Knit_i.jpeg';
                $('#rollname').text('No Data');
                $('#captureAt').text('No Data');
                $('#defectname').text('No Data');

                var rdate = selectElement.value;
                console.log("selectElement.value; : ",selectElement.value)
        
                if (rdate ===""){
                    console.log('Selected date: Empty', rdate);
                    swal({
                        title: "alert!",
                        text: "Please Enter the Valid Roll Number.",
                        type: "warning",
                        timer: 2000
                      });
        
                }else{
                    console.log('Selected Rollnumber: ', rdate);
                    $.ajax({
                        url: '/getdefectlog/'+rdate, // Replace with your API endpoint
                        method: 'POST', // or 'POST' as needed
                        success: function (data) {
                            var jsonObject = JSON.parse(data);
                            let currentIndex = 0;
                            try{
                                $('#rollname').text(jsonObject[currentIndex].roll_name);
                                $('#captureAt').text(jsonObject[currentIndex].timestamp);
                                $('#defectname').text(jsonObject[currentIndex].defect_name);
                            slideImg.src = jsonObject[currentIndex].src;
                            }catch (error) {
                                slideImg.src = '../static/images/Knit_i.jpeg';
                                $('#rollname').text('No Data');
                                $('#captureAt').text('No Data');
                                $('#defectname').text('No Data');
                                console.error('An error occurred:', error.message);                            
    
                            }
                            nextButton.addEventListener('click', () => {
                                try {
                                    if (currentIndex < jsonObject.length - 1) {
                                        currentIndex++;
                                        $('#rollname').text(jsonObject[currentIndex].roll_name);
                                        $('#captureAt').text(jsonObject[currentIndex].timestamp);
                                        $('#defectname').text(jsonObject[currentIndex].defect_name);
                                        slideImg.src = jsonObject[currentIndex].src;
                                    }
                                } catch (error) {
                                    console.error('An error occurred:', error.message);
                                }
                                
                            });
                            preButton.addEventListener('click', () => {
                                try {
                                    if (currentIndex > 0) {
                                        currentIndex--;
                                        $('#rollname').text(jsonObject[currentIndex].roll_name);
                                        $('#captureAt').text(jsonObject[currentIndex].timestamp);
                                        $('#defectname').text(jsonObject[currentIndex].defect_name);
                                        slideImg.src = jsonObject[currentIndex].src;
                                    }
                                } catch (error) {
                                    console.error('An error occurred:', error.message);
                                }
                                
                            });
                        },
                        error: function (error) {
                            console.log("Error value")
                            slideImg.src = '../static/images/Knit_i.jpeg';
                            $('#rollname').text('HIIIII ');
                            $('#captureAt').text(jsonObject[currentIndex].timestamp);
                            $('#defectname').text(jsonObject[currentIndex].defect_name);
                            console.error('Error:', error);
                            swal({
                                title: "alert!",
                                text: "Not able to show Defect.",
                                timer: 2000
                              });
                        }
                    });
                }
            });
        }
    });
    
    const preButton = document.getElementById('pre-button');
    const nextButton = document.getElementById('next-button');    
    var defectLogButton = document.getElementById('getdefectlog_submit');
    var slideImg = document.getElementById('image-slide');
    
    // selectElement.addEventListener('change', function () {
    //     // Get the selected date from the input element
    //     // var rdate = document.getElementById('cars').value;
    //     var rdate = selectElement.value;
    //     console.log("selectElement.value; : ",selectElement.value)

    //     if (rdate ===""){
    //         console.log('Selected date: Empty', rdate);
    //         swal({
    //             title: "alert!",
    //             text: "Please Enter the Valid Roll Number.",
    //             type: "warning",
    //             timer: 2000
    //           });

    //     }else{
    //         console.log('Selected Rollnumber: ', rdate);
    //         $.ajax({
    //             url: '/getdefectlog/'+rdate, // Replace with your API endpoint
    //             method: 'POST', // or 'POST' as needed
    //             success: function (data) {
    //                 var jsonObject = JSON.parse(data);
    //                 let currentIndex = 0;
    //                 $('#rollname').text(jsonObject[currentIndex].roll_name);
    //                 $('#captureAt').text(jsonObject[currentIndex].timestamp);
    //                 $('#defectname').text(jsonObject[currentIndex].defect_name);
    //                 slideImg.src = jsonObject[currentIndex].src;
    //                 nextButton.addEventListener('click', () => {
    //                     try {
    //                         if (currentIndex < jsonObject.length - 1) {
    //                             currentIndex++;
    //                             $('#rollname').text(jsonObject[currentIndex].roll_name);
    //                             $('#captureAt').text(jsonObject[currentIndex].timestamp);
    //                             $('#defectname').text(jsonObject[currentIndex].defect_name);
    //                             slideImg.src = jsonObject[currentIndex].src;
    //                         }
    //                     } catch (error) {
    //                         console.error('An error occurred:', error.message);
    //                     }
                        
    //                 });
    //                 preButton.addEventListener('click', () => {
    //                     try {
    //                         if (currentIndex > 0) {
    //                             currentIndex--;
    //                             $('#rollname').text(jsonObject[currentIndex].roll_name);
    //                             $('#captureAt').text(jsonObject[currentIndex].timestamp);
    //                             $('#defectname').text(jsonObject[currentIndex].defect_name);
    //                             slideImg.src = jsonObject[currentIndex].src;
    //                         }
    //                     } catch (error) {
    //                         console.error('An error occurred:', error.message);
    //                     }
                        
    //                 });
    //             },
    //             error: function (error) {
    //                 console.error('Error:', error);
    //                 swal({
    //                     title: "alert!",
    //                     text: "Not able to show Defect.",
    //                     timer: 2000
    //                   });
    //             }
    //         });
    //     }
    // });

    });

  