$(document).ready(function() {

var downloadPdf = document.getElementById('downloadreport');
// var generateshiftA_ReportButton = document.getElementById('generateshiftA_ReportButton');



downloadPdf.addEventListener('click', function () {
    setTimeout(function() {
        // swal("Loading....!", "Finding USB Drive, please wait!", "info");
        swal({
            title: "Loading....!",
            text: "Finding USB Drive, please wait!",
            type: "info",
            showConfirmButton: false,
            timer: 5000
          });   
        }, 10);

        
    console.log('clicked');
    // Get the selected date from the input elemen
    $.ajax({
        url: '/downloadReport', // Replace with your API endpoint
        method: 'POST', // or 'POST' as needed
        success: function (data) {
            console.log("startNewRollUpdate has been Done!");  
            var data  = data.status
            console.log('*************',data,'************')
            // if(data==true){
            //     setTimeout(function() {
            //         swal("Your Pendrive has been Authdicated!", "Copying report  inprogress please Wait!", "success")
            //         }, 5000);
            //     swal("Good job!", "Your Report has been Downloaded in authdicated Pendrive!", "success")
            //     data = null;
            //     setTimeout(function() {
            //         window.location.replace('pdfViewer');
            //         }, 2000);
            // }else{
            //     swal("Alert!", "No Valid Pendrive Found!", "error")
            // }

            if (data == true) {
                swal("Your Pendrive has been Authenticated!", "Copying report in progress. Please wait!", "success");
            
                setTimeout(function() {
                    swal("Good job!", "Your Report has been Downloaded in authenticated Pendrive!", "success");
                    setTimeout(function() {
                        window.location.replace('pdfViewer');
                    }, 10000);
                }, 1000);
            
                data = null;
            } else {
                swal("Alert!", "No Valid Pendrive Found!", "error");
            }
            
            
        },
        error: function (error) {
            console.error('Error:', error);
            swal({
                title: "alert!",
                text: "Not able to Transfer Report (Try after Some Time).",
                timer: 2000
                });
        }
    });
    
    });
});