<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;

class CreateProxyLink extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:link:proxy';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create a symbolic link to the proxy directory';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Link proxy to the api directory
        $target = base_path('public/proxies');
        $link = base_path('scraper/proxies');

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
