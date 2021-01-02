import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom';
import SearchPage from "../Pages/Search";

export default (props) => {
  return (
    <Router>
      <Switch>
        <Route path="/">
          <SearchPage />
        </Route>
      </Switch>
    </Router>
  );
}