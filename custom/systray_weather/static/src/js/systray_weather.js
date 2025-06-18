/* odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class SystrayWeather extends Component {
    static components = { Dropdown };
    static props = [];
    static template = "SystrayWeather";


    setup() {
        super.setup();
        onMounted(this.onMounted);
        this.weatherData = null;
        this.state = useState({'api':null, 'city': null})
        this.dropdown = useDropdownState();
        this.notification = useService("notification");
    }

    showNotification() {
       this.notification.add(`No city found like ${this.state.city}. Fetching current location.`, {
           title: "Weather Notification",
           type: "info",
           sticky: false,
       });
    }

    getCurrentLocation() {
        const options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0,
        };

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.updateLocation.bind(this), this.handleLocationError.bind(this), options);
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    }

    updateLocation(position) {
        let url = 'https://api.openweathermap.org/data/2.5/weather?';
        const latitude = position?.coords.latitude;
        const longitude = position?.coords.longitude;
        url = (latitude && longitude) ? url + `lat=${latitude}&lon=${longitude}` : url + `q=${this.state.city}`;

        fetch(`${url}&appid=${this.state.api}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                this.weatherData = {
                    'name': data.name,
                    'current_date':`${new Date().getDate()} ${new Date().toLocaleString('en-IN',{month:'long'})} ${new Date().getFullYear()}`,
                    'date': new Date(data.dt * 1000).toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }),
                    'temp': Math.round((data.main.feels_like - 273.15  + Number.EPSILON) * 100) / 100,
                    'weather': data.weather[0].main,
                    'weather_description': data.weather[0].description.charAt(0).toUpperCase() + data.weather[0].description.slice(1),
                    'img_url': `http://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`,

                }
                console.log(data);
            })
            .catch(error => {
                console.warn(error);
                this.showNotification()
                this.getCurrentLocation()
            });
    }

    handleLocationError(error) {
        console.log(error)
    }

     onMounted() {
        rpc("/api/openweather/credentials", {}).then((data) => {
            console.log(data)
            if(data){
                if (data.api_key) this.state.api = data.api_key
                if (data.location?.name) this.state.city = data.location.name
                this.state.city ? this.updateLocation() : this.getCurrentLocation()
            } else {
                registry.category("systray").remove("systray_weather")
            }
        });
    }
}

registry.category("systray").add("systray_weather", { Component: SystrayWeather }, { sequence: 20 });

