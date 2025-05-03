<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;

class CreateMmdbLink extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:link:mmdb';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create a symbolic link to the mmdb directory';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Link proxy to the api directory
        $target = storage_path('app/private/geoip');
        $link = base_path('scraper/mmdb');

        if (! file_exists($target)) {
            $this->error("The target [$target] does not exist.");

            return;
        }

        if (file_exists($link)) {
            $this->error("The link [$link] already exists.");

            return;
        }

        // Create the symbolic link
        if (! file_exists($target)) {
            File::makeDirectory($target, 0755, true);
        }

        if (file_exists($link)) {
            $this->error("The link [$link] already exists.");

            return;
        }
        
        symlink($target, $link);
        
        if (! file_exists($link)) {
            $this->error("Failed to create the link [$link].");

            return;
        }
        
        $this->info("The link [$link] has been created successfully.");
        $this->info("The target [$target] is linked to [$link].");
    }
}
