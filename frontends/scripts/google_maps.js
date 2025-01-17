export function initAutocomplete(apiKey, mapId) {
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
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=initializeMap`;
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

      const input = document.getElementById("searchBox");
      const mapContainer = document.getElementById("map");

      // 初始化地圖和標記
      const defaultLocation = { lat: 25.033964, lng: 121.564468 }; // 預設台北
      const map = new google.maps.Map(mapContainer, {
        center: defaultLocation,
        zoom: 13,
        mapId: mapId,
      });
      const marker = new google.maps.Marker({
        map: map,
        position: defaultLocation,
        draggable: true,
      });

      // 初始化自動完成
      const autocomplete = new google.maps.places.Autocomplete(input);
      autocomplete.bindTo("bounds", map);

      const geocoder = new google.maps.Geocoder();
      const infoWindow = new google.maps.InfoWindow();

      // 如果有預設值，更新地圖位置
      if (input.value) {
        geocoder.geocode({ address: input.value }, (results, status) => {
          if (status === "OK" && results[0].geometry) {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(17);
            marker.setPosition(location);
          }
        });
      }

      // 當選擇新地址時更新地圖和標記
      autocomplete.addListener("place_changed", () => {
        infoWindow.close();

        const place = autocomplete.getPlace();
        if (!place.geometry) {
          console.error("無法獲取地點幾何信息：" + place.name);
          return;
        }

        map.setCenter(place.geometry.location);
        map.setZoom(17);
        marker.setPosition(place.geometry.location);

        infoWindow.setContent(`
          <div>
            <strong>${place.name}</strong><br>
            ${place.formatted_address || ""}
          </div>
        `);
        infoWindow.open(map, marker);
      });

      // 當標記被拖動時，更新輸入框地址
      marker.addListener("dragend", () => {
        const position = marker.getPosition();

        geocoder.geocode({ location: position }, (results, status) => {
          if (status === "OK" && results[0]) {
            input.value = results[0].formatted_address;
          }
        });
      });
    } catch (error) {
      console.error("地圖初始化錯誤：", error);
    }
  }

  initialize();
}
