<script>
    document.getElementById('registrationForm').addEventListener('submit',function(event)
    {
        event.preventDefault();
        //Get form values
        const name=document.getElementById('name').value;
        const branch=document.getElementById('branch').value;
        const score=document.getElementById('score').value;

        //Create a new table row
        const table=document.querySelector('table');
        const newRow=table.insertRow();

        //Insert cells into the new row
        const SlNoCell=newRow.insertCell(0);
        const nameCell=newRow.insertCell(1);
        const branchCell=newRow.insertCell(2);
        const scoreCell=newRow.insertCell(3);

        //Add data to the Cells
        const rowCount=table.rows.length=-1;
        SlNoCell.textContent=rowcount;
        nameCell.textContent=name;
        branchCell.textContent=branch;
        scoreCell.textContent=score;

        //Apply the class to the new row
        newRow.classList.add('dec');

        //Clear the form
        document.getElementById('registrationForm').reset();

    });
</script>