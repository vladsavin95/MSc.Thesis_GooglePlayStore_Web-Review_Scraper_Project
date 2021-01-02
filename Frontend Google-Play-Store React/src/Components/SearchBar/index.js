import React from 'react';

const SearchBar = (props) => {
  return (
    <div className="flex bg-gray-100 h-12 mt-16 mb-12 w-9/12 mx-auto rounded-full hover:shadow-lg">
      <input
        className="w-full focus:outline-none bg-gray-100 rounded-l-full px-8"
        value={props.appLink}
        onChange={props.handleOnAppLinkChange}
        name="appLink"
        placeholder="Enter the app link here..."
      />
      <button
        className={`focus:outline-none bg-gray-200 font-bold px-4 text-gray-400 hover:bg-gray-300 hover:shadow-xl hover:text-white rounded-r-full ${props.loading && 'cursor-wait'}`}
        disabled={props.loading}
        onClick={props.handleOnSearchPress}
      >
        Search
      </button>
    </div>
  )
}

export default SearchBar;