export function initAutocomplete(apiKey) {
  function loadGoogleMapsAPI() {
    return new Promise((resolve, reject) => {
      if (window.google && window.google.maps) {
        resolve(window.google.maps);
        return;
      }

      window.initializeMap = () => {
        resolve(window.google.maps);
      };

      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places,marker&callback=initializeMap`;
      script.async = true;
      script.defer = true;

      script.onerror = () => {
        reject(new Error("Google Maps API 載入失敗"));
      };

      document.head.appendChild(script);
    });
  }

  async function initialize() {
    try {
      await loadGoogleMapsAPI();

      const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 25.033964, lng: 121.564468 },
        zoom: 14,
        mapId: "6a3b782ec188f026",
      });

      const input = document.getElementById("searchBox");
      const autocomplete = new google.maps.places.Autocomplete(input);

      autocomplete.bindTo("bounds", map);

      const infoWindow = new google.maps.InfoWindow();

      // 創建標記但先不設置在地圖上
      let marker = null;

      autocomplete.addListener("place_changed", () => {
        infoWindow.close();

        // 如果標記存在，先從地圖上移除
        if (marker) {
          marker.map = null;
        }

        const place = autocomplete.getPlace();
        if (!place.geometry) {
          console.error("No details available for input: '" + place.name + "'");
          return;
        }

        map.setCenter(place.geometry.location);
        map.setZoom(14);

        // 建立新的標記
        marker = new google.maps.marker.AdvancedMarkerElement({
          map: map,
          position: place.geometry.location,
        });

        infoWindow.setContent(`
                  <div>
                      <strong>${place.name}</strong><br>
                      ${place.formatted_address || ""}
                  </div>
              `);

        infoWindow.setPosition(place.geometry.location);
        infoWindow.open(map);
      });
    } catch (error) {
      console.error("初始化地圖時發生錯誤:", error);
    }
  }

  initialize();
}
