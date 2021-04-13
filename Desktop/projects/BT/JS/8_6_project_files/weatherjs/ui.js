class UI {
    constructor() {
        this.location = document.getElementById('w-location');
        this.desc = document.getElementById('w-desc');
        this.string = document.getElementById('w-string');
        this.details = document.getElementById('w-details');
        this.icon = document.getElementById('w-icon');
        this.humidity = document.getElementById('w-humidity');
        this.feelsLike = document.getElementById('w-feels-like');
        this.temp_min = document.getElementById('w-temp_min');
        this.temp_max = document.getElementById('w-temp_max');
        this.wind = document.getElementById('w-wind');
        this.pressure = document.getElementById('w-pressure');
    }

    paint(weather) {
        this.location.textContent = weather.name;
        this.desc.textContent = `${weather.weather[0].description}`;
        this.string.textContent = weather.temperature_string;
        this.icon.setAttribute('src', weather.icon);
        this.humidity.textContent = `Relative Humidity: ${weather.main.humidity}`;
        this.pressure.textContent = `Pressure: ${weather.main.pressure} Millibars`;
        this.feelsLike.textContent = `Feels Like: ${weather.main.temp} K`;
        this.temp_min.textContent = `Temp min: ${weather.main.temp_min} K`;
        this.temp_max.textContent = `Temp max: ${weather.main.temp_max} k`;
        this.wind.textContent = `Wind: ${weather.wind.speed}`;

    }
}