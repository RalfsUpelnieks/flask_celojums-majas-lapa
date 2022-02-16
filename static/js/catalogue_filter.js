$("#submit-button").click(() => {
    var from = $("#from").find(":selected").val()
    var to = $("#to").find(":selected").val()
    var from_date = $("#from_date").val()
    var to_date = $("#to_date").val()
    $.ajax({
        type: "POST",
        url: "catalogue_filter",
        data: {
            "from": from,
            "to":  to,
            "from_date": from_date,
            "to_date": to_date
        },
        success: (response) => {
            if(response.length == 0) {
                $("#catalogue-list").html('<h3 style="text-align: center;">Nav rezultāta :(</h3>')
                return 0
            }
            $("#catalogue-list").html('')
            response.forEach(element => {
                var trip = `
                    <div class="catalogue-list-element">
                        <img src="/static/images/destinations/${ element.img_file }" class="catalogue-list-element-img">\
                        <div class="catalogue-list-element-text">
                            <h2>${ element.country_from } - ${ element.country_to }</h2>
                            <p>${ element.description }</p>
                            <h2>${ element.cost }€</h2>
                            <p>${ element.date_from } - ${ element.date_to }</p>
                        </div>
                        <a href="/reservation/${ element.id }" class="button" id="button-reserve">Rezervēt</a>
                    </div>
                `
                $("#catalogue-list").append(trip)
            });
        }
    })
})