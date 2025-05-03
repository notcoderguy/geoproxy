<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

class CreateDatabaseLink extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:link:database';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create a symbolic link to the database directory';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Link database.sqlite to the api directory
        $target = base_path('database/database.sqlite');
        $link = base_path('scraper/database.sqlite');
        
        if (! file_exists($target)) {
            $this->error("The target [$target] does not exist.");

            return;
        }

        if (file_exists($link)) {
            $this->error("The link [$link] already exists.");

            return;
        }

        // Create the symbolic link
        symlink($target, $link);
        if (! file_exists($link)) {
            $this->error("Failed to create the link [$link].");

            return;
        }
        $this->info("The link [$link] has been created successfully.");
        $this->info("The target [$target] is linked to [$link].");
    }
}
