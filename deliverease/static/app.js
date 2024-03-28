// Vars for tables, alerts, and close buttons
const $close = $('.close')
const $alert = $('.alert')
const $routes = $('.routes-wrap')
const $stops = $('.stops-wrap')
const $drivers = $('.drivers-wrap')
const $search = $('.search-wrap')
const $admins = $('.admins-wrap')

// Vars for add buttons

const $routeAdd = $('.routes-wrap .add')
const $driverAdd= $('.drivers-wrap .add')
const $adminAdd = $('.admins-wrap .add ')
const $addStop = $('.add-stop')

// Vars for forms

const $routeForm = $('.route-form')
const $stopForm = $('.stop-form')
const $driverForm = $('.driver-form')
const $custForm = $('.cust-form')
const $adminForm = $('.admin-form')



// arrays for all components and for forms

const components = [
    $custForm,
    $routes,
    $stops,
    $drivers,
    $admins,
    $routeForm,
    $stopForm,
    $driverForm,
    $adminForm
    
];

const forms = [
    $routeForm,
    $stopForm,
    $driverForm,
    $custForm,
    $adminForm
]

// event listeners for adding and closing things

components.forEach(c => c.on('click','.close', () => c.hide()))
$alert.on('click','.close', () => $alert.hide())

$routeAdd.on('click', function(){
    hideAll(components);
    $routes.show();
    $routeForm.show()
})

$driverAdd.on('click', function(){
    hideAll(components);
    $drivers.show();
    $driverForm.show()
})

$adminAdd.on('click', function(){
    hideAll(components);
    $admins.show();
    $adminForm.show()
})


//function for hiding array of components 

function hideAll(arr) {
    arr.forEach(el => el.hide())
}

// function to run when page loads

function loadDash(){
    hideAll(components);
    $routes.show();
    $stops.show();
    $drivers.show()
}

// #####################################################################

// #####################################################################


loadDash()