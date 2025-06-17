/* odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { useDiscussSystray } from "@mail/utils/common/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { user } from "@web/core/user";

export class SystrayWeather extends Component {
    static components = { Dropdown };
    static props = [];
    static template = "SystrayWeather";


    setup() {
        super.setup();
        onMounted(this.onMounted);
        this.weatherData = null;
        this.state = useState({'api':null, 'city': null, 'state': null, 'country': null})
        this.dropdown = useDropdownState();
    }

    getLocation() {
        if (this.state.city) {
            fetch(`http://api.openweathermap.org/geo/1.0/direct?q=${this.state.city},${this.state.city},${this.state.country}&limit={limit}&appid=${this.state.api}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data)
                });
        } else {
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
    }

    updateLocation(position) {
        const { latitude, longitude } = position.coords;
        const apiKey = '39935437eb2d27164cfb2600006caedd'

        if (!(latitude || longitude)) {
            console.log("No lat log")
            return
        }

        fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`)
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
                console.error('There was a problem with the fetch operation:', error);
            });


    }

    handleLocationError(error) {
        console.log(error)
    }

     onMounted() {
        rpc("/api/openweather/credentials", {}).then((data) => {
            console.log(data)
            if (data.api_key) this.state.api = data.api_key
            if (data.location?.name) this.state.city = data.location.name
            if (data.location?.state) this.state.state = data.location.state
            if (data.location?.country) this.state.country = data.location.country
            this.getLocation()
        });
    }
}

registry
    .category("systray")
    .add("systray_weather", { Component: SystrayWeather }, { sequence: 20 });

