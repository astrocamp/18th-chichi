export function showMap(apiKey, mapId, address) {
  function loadGoogleMapsAPI() {
    return new Promise((resolve, reject) => {
      if (window.google && window.google.maps) {
        resolve(window.google.maps);
        return;
      }

      // 載入完成後執行的 callback
      window.initializeMap = () => resolve(window.google.maps);

      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initializeMap`;
      script.async = true;
      script.defer = true;
      script.onerror = () => reject(new Error("Google Maps API 載入失敗"));
      document.head.appendChild(script);
    });
  }

  // 2. 初始化地圖
  async function initialize() {
    try {
      const googleMaps = await loadGoogleMapsAPI();

      // 建立地圖，可先放全球視野
      const map = new googleMaps.Map(document.getElementById("map"), {
        center: { lat: 25.033964, lng: 121.564468 },
        zoom: 2,
        mapId: mapId || undefined,
      });

      // 如果有地址，就用 Geocoding 定位
      if (address) {
        const geocoder = new googleMaps.Geocoder();
        geocoder.geocode({ address }, (results, status) => {
          if (status === "OK") {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(14);

            // 放個 Marker
            new googleMaps.Marker({
              map,
              position: location,
              title: address,
            });
          } else {
            console.error("Geocode失敗:", status);
          }
        });
      }
    } catch (error) {
      console.error("初始化地圖時發生錯誤:", error);
    }
  }

  // 3. 執行
  initialize();
}
