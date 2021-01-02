import React, { useState } from 'react';
import axios from 'axios';
import {
  SearchBar
} from "../../Components";
import { apiUrl } from "../../config";
import LoadingImage from "../../assets/loading.png";

const Search = (props) => {

  const [words, setWords] = useState("");
  const [maxwords, setMaxWords] = useState(300);
  const [mask, setMask] = useState("heart");
  const [appLink, setAppLink] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState(null);
  const [dataResponse, setdataResponse] = useState(null)
  const [color, setColor] = useState('default')
  const [font, setFont] = useState('default')
  const [corpus, setCorpus] = useState('english')

  const colors = ['default', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap',
    'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r',
    'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2',
    'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
    'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
    'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
    'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
    'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr',
    'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r',
    'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
    'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern',
    'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray',
    'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r',
    'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism',
    'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r',
    'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
    'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis',
    'viridis_r', 'winter', 'winter_r']

  const fonts = ['default', 'Fresh Lychee', 'Heysweet', 'Remachine Script']


  const handleOnAppLinkChange = (e) => {
    setAppLink(e.target.value);
  }

  const handleOnMaskChange = (e) => {
    setMask(e.target.value);
  }

  const handleOnColorChange = (e) => {
    setColor(e.target.value);
  }

  const handleOnFontChange = (e) => {
    setFont(e.target.value);
  }

  const handleOnWordsChange = (e) => {
    setWords(e.target.value);
  }

  const handleOnMaxWordsChange = (e) => {
    setMaxWords(e.target.value);
  }

  const handleOnCorpusChange = (e) => {
    setCorpus(e.target.value);
  }

  const handleOnSearchPress = () => {
    setLoading(true);
    setSearchResults(null);
    setdataResponse(null)
    let data ={
      appLink,
      words,
      mask,
      color,
      font,
      maxwords,
      corpus,
      dataResponse,
    };
    axios.post(`${apiUrl}/search`, data).then((response)=>{
      setAppLink("")
      if(response.data.type === "success") {
        setSearchResults(response.data.search_results);
        setdataResponse(response.data);
      } else {
        alert(`Error: ${response.data.message}`);
      }
      setLoading(false);
    });
  }

  return (
    <div className="w-screen h-screen bg-white text-xl text-gray-500">
      <SearchBar
        appLink={appLink}
        loading={loading}
        handleOnSearchPress={handleOnSearchPress}
        handleOnAppLinkChange={handleOnAppLinkChange}
      />
      <div className="flex justify-between h-12 mt-16 mb-12 w-9/12 mx-auto" style={{flex:1,justifyContent: "center",alignItems: "center"}}>
        <div className="flex items-center">
          <span className="px-3">Mask:</span>
          <select
            className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
            onChange={handleOnMaskChange}
          >
            <option selected={mask === "heart" ? true : false} value="heart">Heart</option>
            <option selected={mask === "cloud" ? true : false} value="cloud">Cloud</option>
            <option selected={mask === "comment" ? true : false} value="comment">Comment</option>
            <option selected={mask === "like" ? true : false} value="like">Like</option>
            <option selected={mask === "location" ? true : false} value="location">Location</option>
            <option selected={mask === "star" ? true : false} value="star">Star</option>
            <option selected={mask === "user" ? true : false} value="user">User</option>
            <option selected={mask === "android" ? true : false} value="android">Android</option>
            <option selected={mask === "diamond" ? true : false} value="diamond">Diamond</option>
          </select>
          <span className="px-3">Color:</span>
          <select
              className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
              onChange={handleOnColorChange}
          >
            {colors.map(c =>
                <option selected={color === c ? true : false} value={c}>{c}</option>
            )};
          </select>

          <span className="px-3">Font:</span>
          <select
              className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
              onChange={handleOnFontChange}
          >
            {fonts.map(f =>
                <option selected={font === f ? true : false} value={f}>{f}</option>
            )};
          </select>

        </div>
      </div>
      <div className="flex justify-between h-12 mt-16 mb-12 w-9/12 mx-auto" style={{flex:1,justifyContent: "center",alignItems: "center"}}>
        <div className="flex items-center">
          <span className="px-3">Block Words:</span>
          <input
            className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
            onChange={handleOnWordsChange}
            placeholder="Type here comma separated words..."
            value={words}
          />
          <span className="px-3">Max Words:</span>
          <input
              className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
              onChange={handleOnMaxWordsChange}
              placeholder="Type here comma separated words..."
              value={maxwords}
          />
          <span className="px-3">Corpus:</span>
          <select
              className={`focus:outline-none bg-gray-100 py-2 px-4 ${loading && 'cursor-wait'}`}
              onChange={handleOnCorpusChange}
          >
            <option selected={mask === "english" ? true : false} value="english">English</option>
            <option selected={mask === "french" ? true : false} value="french">French</option>
          </select>
        </div>
      </div>
      {
        loading
          ?
            <div className="flex justify-center items-center h-48">
              <img style={{width: 25}} className="animate-spin mr-3" src={LoadingImage} />
              <h2>Please hold on, data is being processed...</h2>
            </div>
          :
            searchResults && Object.keys(searchResults).length > 0
              &&
                <center>
                  <button onClick={handleOnSearchPress}>Change mask</button>
                  {
                    searchResults?.neutral_wordcloud_image
                      &&
                        <div>
                          <p className="mt-4 mb-8 text-xl font-bold">Neutral Word Cloud</p>
                          <img src={`${apiUrl}/${searchResults.neutral_wordcloud_image}`} />
                        </div>
                  }
                  {
                    searchResults?.positive_wordcloud_image
                      &&
                        <div>
                          <p className="mt-4 mb-8 text-xl font-bold">Positive Word Cloud</p>
                          <img src={`${apiUrl}/${searchResults.positive_wordcloud_image}`} />
                        </div>
                  }
                  {
                    searchResults?.negative_wordcloud_image
                      &&
                        <div>
                          <p className="mt-4 mb-8 text-xl font-bold">Negative Word Cloud</p>
                          <img src={`${apiUrl}/${searchResults.negative_wordcloud_image}`} />
                        </div>
                  }
                  <div className="mt-16 mb-8">
                    <p className="text-xl font-bold">Histogram</p>
                    <img src={`${apiUrl}/${searchResults.histogram_image}`} />
                  </div>
                </center>
      }
      <div>

      </div>
    </div>
  );
}

export default Search;