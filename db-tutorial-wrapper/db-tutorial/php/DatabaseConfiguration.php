<?php
class DatabaseConfiguration
{
    protected $servername;
    protected $username;
    protected $password;
    protected $dbname;
    protected $portnumber;

    public function __construct()
    {
        $this->servername = "localhost";
        $this->username = "<mysqlusername>";
        $this->password = "<mysqluserpw>";
        $this->dbname = "website_tutorial";
        $this->portnumber = "22";
    }

    public function createConnection() {

        // Create connection
        $conn = mysqli_connect($this->servername, $this->username, $this->password, $this->dbname, $this->portnumber);

        // Check connection
        if (!$conn) {
            die('Could not connect: ' . mysqli_error($conn));
        }

        return $conn;
    }
}
