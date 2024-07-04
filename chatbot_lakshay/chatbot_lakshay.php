<?php
/*
Plugin Name: chatbot_lakshay
Description: llm chatbot
Author: lakshay
version: 1.0.0
Text Domain: chatbot
*/

// Enqueue the necessary scripts and styles
function chatbot_lakshay_enqueue_scripts() {
    wp_enqueue_script('jquery');
}
add_action('wp_enqueue_scripts', 'chatbot_lakshay_enqueue_scripts');

// Create a shortcode to display the Streamlit app
function chatbot_lakshay_shortcode() {
    // Get the site URL
    $site_url = site_url();

    ob_start();
    ?>
    <div id="chatbot-lakshay-container" style="width: 100%; height: 1000px;">
        <iframe src="http://localhost:8501" width="100%" height="100%" frameborder="0"></iframe>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('chatbot_lakshay', 'chatbot_lakshay_shortcode');

// Add a settings page for the plugin
function chatbot_lakshay_add_admin_menu() {
    add_options_page('Chatbot Lakshay', 'Chatbot Lakshay', 'manage_options', 'chatbot_lakshay', 'chatbot_lakshay_options_page');
}
add_action('admin_menu', 'chatbot_lakshay_add_admin_menu');

function chatbot_lakshay_options_page() {
    ?>
    <div class="wrap">
        <h1>Chatbot Lakshay Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('chatbot_lakshay_options_group');
            do_settings_sections('chatbot_lakshay');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// Register settings
function chatbot_lakshay_settings_init() {
    register_setting('chatbot_lakshay_options_group', 'chatbot_lakshay_url');

    add_settings_section(
        'chatbot_lakshay_section',
        __('Chatbot Lakshay Settings', 'wordpress'),
        'chatbot_lakshay_section_callback',
        'chatbot_lakshay'
    );

    add_settings_field(
        'chatbot_lakshay_url',
        __('Streamlit App URL', 'wordpress'),
        'chatbot_lakshay_url_render',
        'chatbot_lakshay',
        'chatbot_lakshay_section'
    );
}
add_action('admin_init', 'chatbot_lakshay_settings_init');

function chatbot_lakshay_section_callback() {
    echo __('Enter the URL of your Streamlit chatbot app.', 'wordpress');
}

function chatbot_lakshay_url_render() {
    $url = get_option('chatbot_lakshay_url');
    ?>
    <input type='text' name='chatbot_lakshay_url' value='<?php echo esc_attr($url); ?>' size='50'>
    <?php
}
?>