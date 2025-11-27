<?php

$insert = false;
$update = false;
$delete = false;



$server = "localhost";
$username = "root";
$pass = "";

$database = "ToDolist";
    echo "  succuessfuly created database <br>";
$con = mysqli_connect($server, $username, $pass,$database);

// $sql = "create database ToDolist";
// $resdata = mysqli_query($con, $sql);
// if ($resdata) {

//     echo "  succuessfuly created database <br>";
// } else {

//     echo "  notcreated database <br>";
// }





if (!$con) {
    die("failed connection " . mysqli_connect_error());
} else {
    // echo "connection was successful<br>";
}




// $sql="create table info(
//     Id int auto_increment primary key not null,
//     Title nvarchar(100), description Text(10000),
//     date DATETIME DEFAULT current_timestamp())";

// $resdata = mysqli_query($con, $sql);
// if ($resdata) {

//     echo "  succuessfuly created table <br>";
// } else {

//     echo "  notcreated table <br>";
// }


if (isset($_GET['delete'])) {

    $sno = $_GET['delete'];
    $sql = "Delete from info where Id= $sno";
    $result = mysqli_query($con, $sql);
    $delete = true;
}



if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['editid'])) {


        $id = $_POST['editid'];
        $title = $_POST['titleEdit'];
        $des = $_POST['desEdit'];

        $updatequery = "update info set Title='$title', description ='$des' where info.id='$id'";
        $result = mysqli_query($con, $updatequery);
        if ($result) {
            $update = true;
        } else {
            echo "not updated";
        }
    }


    // delete  all data 
    else if (isset($_POST['del'])) {


        $sql = "Delete from info";
        $result = mysqli_query($con, $sql);
        $delete = true;
    }

    // post  all data 
    else {
        $title = $_POST['title'];
        $des = $_POST['des'];
        $sql = "Insert into info(title, description)values('$title', '$des')";
        $res = mysqli_query($con, $sql);

        if ($res) {
            // echo "  succuessfuly inserted <br>";
            $insert = true;
        } else {

            echo "  not inserted <br>";
        }
    }
}
?>
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <!-- jquery -->
    <link rel="stylesheet" href="//cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css">
</head>
<style>
    body {
        /* background-image: url('https://images.unsplash.com/photo-1622126807280-9b5b32b28e77?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1160&q=80');
        background-size: cover; */
    }
</style>

<body>

    <!-- Button trigger modal -->
    <!-- <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editModal">
        Launch demo modal
    </button> -->

    <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="editModalLabel">My Note </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">

                    <form action="main.php" method="POST">
                        <!-- for fetech data -->
                        <input type="hidden" name="editid" id="editid">
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" class="form-control" id="titleEditt" name="titleEdit" aria-describedby="emailHelp">

                        </div>
                        <div class="form-floating">
                            <textarea class="form-control" placeholder="Leave a comment here" name="desEdit" id="desEdit"></textarea>
                            <label for="des">Description</label>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Save changes</button>
                        </div>
                    </form>

                </div>

            </div>
        </div>
    </div>

    <nav class="navbar navbar-expand-lg  navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Link</a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link disabled">contact</a>
                    </li>
                </ul>
                <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>


    <?php
    if ($insert) {
        echo "<div class='alert alert-success alert-dismissible fade show' role='alert'>
    <strong>Success!</strong> Your task has been successfully added.
    <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>
   </div>";
    }
    ?>

    <?php
    if ($update) {
        echo "<div class='alert alert-primary alert-dismissible fade show' role='alert'>
    <strong>Success!</strong> Your task has been successfully updated.
    <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>
   </div>";
    }
    ?>

    <?php
    if ($delete) {
        echo "<div class='alert alert-danger alert-dismissible fade show' role='alert'>
    <strong>Success!</strong> Your task has been successfully deleted.
    <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>
   </div>";
    }
    ?>
    <div class="container" style="margin-top: 50px ; background-color: transparent;">
        <div class="container" style="margin-top: 50px ;">
            <h1>My To Do App</h1>
            <form action="main.php" method="POST">
                <div class="mb-3">
                    <label for="title" class="form-label">Title</label>
                    <input type="text" class="form-control" id="title" name="title" aria-describedby="emailHelp">

                </div>
                <div class="form-floating">
                    <textarea class="form-control" placeholder="Leave a comment here" name="des" id="des"></textarea>
                    <label for="des">Description</label>
                </div>
                <div class="d-grid gap-2 col-6 mx-auto">
                    <button style="margin-top: 10px ;" type="submit" class="btn btn-primary">Submit</button>
                </div>
            </form>
        </div>
        <div class="container" style="margin-top: 50px ;">
            <form action="Lecture05ToDoApp.php" method="POST">
                <input type="hidden" name="del">
                <div class="d-grid gap-2 col-6 mx-auto">

                    <button class="btn btn-danger" type="submit">Delete All </button>
                </div>

            </form>
        </div>
    </div>
        <div class="container mt-4 table-success">
            <table id="myTable" class="table table-success table-hover">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Title</th>
                        <th scope="col">Description</th>
                        <th scope="col">Option</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // **** FETCH DATA IN TABULAR FORMAT ****
                    $sqlselect = "select *from info ";
                    $res = mysqli_query($con, $sqlselect);
                    $count = 1;
                    while ($show = mysqli_fetch_assoc($res)) {



                        // echo "<br>total rows".var_dump($show);

                        echo "<tr>
                    
                    <td>" . $count++ . "</td>";
                        echo " <td>" . $show['Title'] . "</td>";
                        echo " <td>" . $show['description'] . "</td>";

                        echo "<td>
                    
                    <button type='button' class='btn btn-primary edit' id=" . $show['Id'] . ">Edit</button>
                    <button type='button' class='btn btn-danger  delete' id=d" . $show['Id'] . ">Delete</button>
                    
                    </td>
                    
                    </tr>";
                    }


                    ?>
                </tbody>
            </table>

        </div>


        <script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
        <script src="//cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js">
        </script>
        <script>
            $(document).ready(function() {
                $('#myTable').DataTable();
            });
        </script>







        <script>
            edits = document.getElementsByClassName('edit');


            Array.from(edits).forEach((element) => {

                element.addEventListener("click", (e) => {

                    // console.log("edit sahi chal raha hai humara mubarak ho", e.target.parentNode.parentNode);
                    // yeh variable name hai or kuch nahi hai 
                    tr = e.target.parentNode.parentNode;
                    title = tr.getElementsByTagName("td")[1].innerText;
                    des = tr.getElementsByTagName("td")[2].innerText;
                    console.log(title, des)
                    titleEditt.value = title;
                    desEdit.value = des;
                    editid.value = e.target.id;
                    console.log("id is working now", e.target.id)
                    $('#editModal').modal('toggle');


                })
            })

            deletes = document.getElementsByClassName('delete');


            Array.from(deletes).forEach((element) => {

                element.addEventListener("click", (e) => {

                    console.log("my delete btn is working ")
                    sno = e.target.id.substr(1);
                    if (confirm("Are you sure want to delete this task")) {
                        console.log("yes");
                        window.location = `/todoweb/main.php?delete=${sno}`;
                    } else {
                        console.log("no")
                    }




                })
            })
        </script>

</body>

</html>