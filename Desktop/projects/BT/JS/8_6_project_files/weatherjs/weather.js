class Weather {
    constructor(city, state) {
        this.apikey = 'afb818e38cd7932e7ae2ba6766a98bb7';
        this.city = city;
        this.state = state;
    }

    // Fetch weather from API
    async getWeather() {
        const response = await fetch(`http://api.openweathermap.org/data/2.5/weather?q=${this.city},${this.state}&appid=${this.apikey}
        `);

        const responseData = await response.json();

        return responseData
    }

    // Change weather location
    changeLocation(city, state) {
        this.city = city;
        this.state = state;
    }
}