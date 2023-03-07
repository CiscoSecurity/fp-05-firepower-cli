export function Output(props) {
  return (
    <tr class="table__row">
      <tr class="table__cell">{props.output.adapter}</tr>
      <tr class="table__cell">{props.output.stream[0].uri}</tr>
      <tr class="table__cell">{props.output.enabled}</tr>
      <button class="btn btn--primary">Run</button>
    </tr>
  );
}
