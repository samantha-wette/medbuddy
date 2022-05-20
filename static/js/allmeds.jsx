function MedContainer() {
    const [medInfo, setMedInfo] = React.useState({});

    React.useEffect(() => {
        fetch('/med-data')
        .then((response) => response.json())
        .then((result) => {
            setMedInfo(result);
        });
    }, []);
    const meds = []; 
    
    if (medInfo.length === 0) {
        return<p>Error, no meds present</p>;
    }
    if ("official" in medInfo) {
        console.log(medInfo)
        for (const currentMed of medInfo.official) {
        meds.push(<div className="card">
            <div className="card-body">
                <h5 className="card-title">{currentMed.name}</h5>
                <a href={currentMed.info} className="btn btn-primary">Learn More</a>
            </div>
            </div>

        )}}
    
    return (
      <React.Fragment>
          All the meds are:
        {meds}
      </React.Fragment>
    );
  }

function Pagination() {
    return <nav aria-label="Page navigation example">
    <ul class="pagination">
      <li class="page-item">
        <a class="page-link" href="#" aria-label="Previous">
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>
      <li class="page-item"><a class="page-link" href="#">1</a></li>
      <li class="page-item"><a class="page-link" href="#">2</a></li>
      <li class="page-item"><a class="page-link" href="#">3</a></li>
      <li class="page-item">
        <a class="page-link" href="#" aria-label="Next">
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </nav>}
  
  ReactDOM.render(<MedContainer />, document.querySelector("#all-meds"));
  ReactDOM.render(<Pagination />, document.querySelector('#pagination'));