"use client";
import React, { useState } from "react";
import { HoveredLink, Menu, MenuItem, ProductItem } from "../components/ui/navbar-menu";
import { HeroParallax } from "../components/ui/hero-parallax";
import { TypewriterEffectSmooth } from "../components/ui/typewriter-effect";
import { TextGenerateEffect } from "../components/ui/text-generate-effect";
import { Footer } from "../components/ui/footer"
import { PinContainer } from "../components/ui/3d-pin";
import { Contact } from "../components/ui/contact";
import { cn } from "@/utils/cn";
import hero from '../../public/hero1.jpeg'

import Image from 'next/image';
function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);
  return (
    <div
      className={cn("fixed top-10 inset-x-0 max-w-2xl mx-auto z-50", className)}
    >
      <Menu setActive={setActive}>
        <MenuItem setActive={setActive} active={active} item="Home">
        </MenuItem>
        <MenuItem setActive={setActive} active={active} item="About">
        </MenuItem>
        <MenuItem setActive={setActive} active={active} item="Services">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/web-dev">Web Development</HoveredLink>
            <HoveredLink href="/interface-design">Interface Design</HoveredLink>
            <HoveredLink href="/seo">Search Engine Optimization</HoveredLink>
            <HoveredLink href="/branding">Branding</HoveredLink>
          </div>
        </MenuItem>
        <MenuItem setActive={setActive} active={active} item="Products">
          <div className="  text-sm grid grid-cols-2 gap-10 p-4">
            <ProductItem
              title="Algochurn"
              href="https://algochurn.com"
              src="https://assets.aceternity.com/demos/algochurn.webp"
              description="Prepare for tech interviews like never before."
            />
            <ProductItem
              title="Tailwind Master Kit"
              href="https://tailwindmasterkit.com"
              src="https://assets.aceternity.com/demos/tailwindmasterkit.webp"
              description="Production ready Tailwind css components for your next project"
            />
            <ProductItem
              title="Tailwind Master Kit"
              href="https://tailwindmasterkit.com"
              src="https://assets.aceternity.com/demos/tailwindmasterkit.webp"
              description="Production ready Tailwind css components for your next project"
            />
            <ProductItem
              title="Rogue"
              href="https://userogue.com"
              src="https://assets.aceternity.com/demos/Screenshot+2024-02-21+at+11.47.07%E2%80%AFPM.png"
              description="Respond to government RFPs, RFIs and RFQs 10x faster using AI"
            />
          </div>
        </MenuItem>
        <MenuItem setActive={setActive} active={active} item="Pricing">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/hobby">Hobby</HoveredLink>
            <HoveredLink href="/individual">Individual</HoveredLink>
            <HoveredLink href="/team">Team</HoveredLink>
            <HoveredLink href="/enterprise">Enterprise</HoveredLink>
          </div>
        </MenuItem>
      </Menu>
    </div>
  );
}


const TwoSectionComponent = () => {
  const words = 'Welcome to Code Omega, where we specialize in crafting cutting-edge AI solutions to revolutionize industries and enhance lives. With a team of seasoned experts and a commitment to innovation, we navigate the complexities of AI development, from machine learning algorithms to neural networks. Our promise is simple: to deliver tailored solutions that empower our clients to unlock new opportunities and achieve unprecedented growth. Join us in shaping the future, where AI meets ingenuity, and possibilities are limitless.';
  return (
    <div className="flex flex-wrap">
      <div className="w-full md:w-1/2 p-4">
        <Image
          src="/hero1.jpg" // Ensure this path is correct and relative to the public directory
          alt="Description of the image"
          width={500} // Specify the width
          height={300} // Specify the height
          layout="responsive" // Use responsive layout for better scaling
        />
      </div>
      <div className="w-full md:w-1/2 p-4">
        <h1 className="text-2xl md:text-7xl font-bold dark:text-white">About Us</h1>
        <TextGenerateEffect words={words} />
      </div>
    </div>

  );
};


export const products = [
  {
    title: "Moonbeam",
    link: "https://gomoonbeam.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/cursor.png",
  },
  {
    title: "Cursor",
    link: "https://cursor.so",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/cursor.png",
  },
  {
    title: "Rogue",
    link: "https://userogue.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/rogue.png",
  },

  {
    title: "Editorially",
    link: "https://editorially.org",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/editorially.png",
  },
  {
    title: "Editrix AI",
    link: "https://editrix.ai",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/editrix.png",
  },
  {
    title: "Pixel Perfect",
    link: "https://app.pixelperfect.quest",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/pixelperfect.png",
  },

  {
    title: "Algochurn",
    link: "https://algochurn.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/algochurn.png",
  },
  {
    title: "Aceternity UI",
    link: "https://ui.aceternity.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/aceternityui.png",
  },
  {
    title: "Tailwind Master Kit",
    link: "https://tailwindmasterkit.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/tailwindmasterkit.png",
  },
  {
    title: "SmartBridge",
    link: "https://smartbridgetech.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/smartbridge.png",
  },
  {
    title: "Renderwork Studio",
    link: "https://renderwork.studio",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/renderwork.png",
  },

  {
    title: "Creme Digital",
    link: "https://cremedigital.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/cremedigital.png",
  },
  {
    title: "Golden Bells Academy",
    link: "https://goldenbellsacademy.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/goldenbellsacademy.png",
  },
  {
    title: "Invoker Labs",
    link: "https://invoker.lol",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/invoker.png",
  },
  {
    title: "E Free Invoice",
    link: "https://efreeinvoice.com",
    thumbnail:
      "https://aceternity.com/images/products/thumbnails/new/efreeinvoice.png",
  },
];

const words = [
  {
    text: "Empowering",
  },
  {
    text: "Your",
  },
  {
    text: "Digital",
  },
  {
    text: "Future",
  },
  {
    text: "With",
  },
  {
    text: "AI",
    className: "text-blue-500 dark:text-blue-500",
  },
];

const LandingPage = () => {
  return (
    <>
      <div className="relative w-full h-[800px]"> {/* Adjust the height as needed */}
        <Image
          src="/hero1.jpeg" // Ensure this path is correct and relative to the public directory
          alt="Hero Image"
          layout="fill"
          objectFit="cover"
          objectPosition="center"
        />
        <div className="absolute inset-0 bg-black opacity-50"></div>
      </div>
      <div className="w-full flex items-center justify-center">
        <Navbar className="top-2" />
      </div>


      <div className="">

        <div className="absolute inset-0 bg-black opacity-40"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="mx-auto max-w-[1200px] text-center text-accent-900 dark:text-white lg:mt-[60px]">
            <div className="space-y-12 md:space-y-12">
              <TypewriterEffectSmooth words={words} />
              <a target="_self" aria-label="Discover More" className="text-white dark:text-white bg-red-800 overflow-hidden text-base leading-[1.1] font-bold font-secondary tracking-wide uppercase [transition:all_0.3s_linear] inline-flex items-center justify-center gap-3 md:min-h-[3.75rem] min-h-[3.5rem] px-6 md:px-7 py-2 md:py-3 transition-colors ease-in-out ring-offset-primary-dark focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 bg-primary after:absolute after:h-full after:w-0 after:bottom-0 after:right-0 after:bg-black/[.15] after:-z-1 after:[transition:all_.3s_ease-in-out] hover:text-white dark:hover:text-white hover:after:w-full hover:after:left-0 rounded-5 rounded-full" href="/">
                <span>Discover More</span>
                <svg width="28" height="9" viewBox="0 0 28 9" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M27.7911 5.02543C27.9863 4.83016 27.9863 4.51358 27.7911 4.31832L24.6091 1.13634C24.4138 0.941077 24.0972 0.941077 23.902 1.13634C23.7067 1.3316 23.7067 1.64818 23.902 1.84345L26.7304 4.67187L23.902 7.5003C23.7067 7.69556 23.7067 8.01214 23.902 8.20741C24.0972 8.40267 24.4138 8.40267 24.6091 8.20741L27.7911 5.02543ZM0.4375 5.17188L27.4375 5.17187L27.4375 4.17187L0.4375 4.17188L0.4375 5.17188Z"></path></svg></a>
            </div>
          </div>
          <div className="pointer-events-none absolute z-1 bottom-0 left-0 right-0 mx-auto hidden lg:block aos-init aos-animate" data-aos="fade-up" data-aos-delay="450">
          </div>
          <span className="pointer-events-none absolute z-1 left-0 top-0 hidden lg:block aos-init aos-animate" data-aos="fade-right" data-aos-delay="200"><svg width="214" height="470" viewBox="0 0 214 470" fill="white" xmlns="http://www.w3.org/2000/svg"><path opacity="0.3" d="M-154.988 -640.533C-246.834 -636.395 -330.486 -574.566 -390.536 -466.574C-450.36 -358.902 -479.66 -218.08 -472.988 -70.0004C-466.315 78.0794 -424.469 215.685 -355.204 317.54C-285.682 419.745 -196.811 473.749 -104.965 469.61C-13.1178 465.472 70.4961 403.695 130.583 295.651C190.427 187.978 219.708 47.1472 213.036 -100.913C206.364 -248.972 164.536 -386.609 95.2513 -488.463C25.6902 -590.666 -63.1409 -644.672 -154.988 -640.533ZM-105.01 468.611C-196.497 472.734 -285.06 418.886 -354.378 316.973C-423.556 215.274 -465.326 77.8246 -471.989 -70.0454C-478.652 -217.915 -449.414 -358.584 -389.663 -466.083C-329.792 -573.817 -246.43 -635.412 -154.943 -639.534C-63.4555 -643.657 25.1082 -589.809 94.3861 -487.894C163.564 -386.195 205.334 -248.746 211.997 -100.866C218.66 47.0142 189.462 187.651 129.671 295.162C69.8394 402.894 -13.5225 464.489 -105.01 468.611Z" className="fill-accent-900 dark:fill-white"></path></svg><span className="absolute left-[125px] top-[215px] z-1"><svg className="animate-rotate-me" width="58" height="59" viewBox="0 0 58 59" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M39.7784 0.611394L22.6412 15.4979L0.18668 18.792L15.0728 35.9193L18.3573 58.3842L35.4946 43.4977L57.9491 40.2036L43.0626 23.0663L39.7784 0.611394Z" fill="white"></path></svg></span></span>
          <span className="pointer-events-none absolute z-1 right-0 top-[60px] hidden lg:block aos-init aos-animate" data-aos="fade-left" data-aos-delay="350">
            <svg width="136" height="869" viewBox="0 0 136 869" fill="white" xmlns="http://www.w3.org/2000/svg"><path opacity="0.3" d="M48.0704 97.0361C-7.79726 170.055 -14.2044 273.878 29.9236 389.295C73.9511 504.333 162.993 617.297 280.717 707.37C398.442 797.442 530.753 853.837 653.301 866.248C776.281 878.688 874.776 845.322 930.644 772.303C986.511 699.284 992.934 595.523 948.791 480.043C904.775 364.99 815.714 252.035 698.005 161.975C580.296 71.9148 447.974 15.4858 325.413 3.09053C202.409 -9.31698 103.938 24.0171 48.0704 97.0361ZM929.85 771.695C874.201 844.428 776.023 877.659 653.397 865.251C531.024 852.874 398.883 796.52 281.325 706.576C163.767 616.631 74.8022 503.813 30.861 388.942C-13.1838 273.828 -6.7843 170.377 48.8646 97.6437C104.513 24.9107 202.691 -8.32025 325.293 4.11942C447.666 16.4969 579.807 72.8502 697.373 162.801C814.939 252.752 903.904 365.519 947.829 480.428C991.898 595.511 985.498 698.962 929.85 771.695Z" className="fill-accent-900 dark:fill-white"></path></svg>
            <span className="absolute right-[80px] top-[350px] z-1">
              <svg
                style={{
                  animation: 'rotate 2s linear infinite',
                  transformOrigin: 'center',
                }}
                width="58"
                height="59"
                viewBox="0 0 58 59"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M39.7784 0.611394L22.6412 15.4979L0.18668 18.792L15.0728 35.9193L18.3573 58.3842L35.4946 43.4977L57.9491 40.2036L43.0626 23.0663L39.7784 0.611394Z" fill="white"></path>
              </svg>
            </span>
          </span>

          <div className="pointer-events-none absolute z-1 bottom-0 left-0 right-0 mx-auto hidden lg:block aos-init aos-animate" data-aos="fade-up" data-aos-delay="450">

            <Image
              src="/bg.jpeg" // Ensure this path is correct and relative to the public directory
              alt="Hero Image"
              style={{ color: "transparent" }}
              height="300"
              width="1920"
            />
          </div>
        </div>
      </div>
      <div className="h-[40rem] w-full flex items-center justify-center flex-wrap">
        <PinContainer
          title="/ui.aceternity.com"
          href="https://twitter.com/mannupaaji"
        >
          <div className="flex basis-full flex-col p-4 tracking-tight text-slate-100/50 sm:basis-1/2 w-[20rem] h-[20rem] ">
            <h3 className="max-w-xs !pb-2 !m-0 font-bold  text-base text-slate-100">
              Aceternity UI
            </h3>
            <div className="text-base !m-0 !p-0 font-normal">
              <span className="text-slate-500 ">
                Customizable Tailwind CSS and Framer Motion Components.
              </span>
            </div>
            <div className="flex flex-1 w-full rounded-lg mt-4 bg-gradient-to-br from-violet-500 via-purple-500 to-blue-500" />
          </div>
        </PinContainer>
        <PinContainer
          title="/ui.aceternity.com"
          href="https://twitter.com/mannupaaji"
        >
          <div className="flex basis-full flex-col p-4 tracking-tight text-slate-100/50 sm:basis-1/2 w-[20rem] h-[20rem] ">
            <h3 className="max-w-xs !pb-2 !m-0 font-bold  text-base text-slate-100">
              Aceternity UI
            </h3>
            <div className="text-base !m-0 !p-0 font-normal">
              <span className="text-slate-500 ">
                Customizable Tailwind CSS and Framer Motion Components.
              </span>
            </div>
            <div className="flex flex-1 w-full rounded-lg mt-4 bg-gradient-to-br from-violet-500 via-purple-500 to-blue-500" />
          </div>
        </PinContainer>
        <PinContainer
          title="/ui.aceternity.com"
          href="https://twitter.com/mannupaaji"
        >
          <div className="flex basis-full flex-col p-4 tracking-tight text-slate-100/50 sm:basis-1/2 w-[20rem] h-[20rem] ">
            <h3 className="max-w-xs !pb-2 !m-0 font-bold  text-base text-slate-100">
              Aceternity UI
            </h3>
            <div className="text-base !m-0 !p-0 font-normal">
              <span className="text-slate-500 ">
                Customizable Tailwind CSS and Framer Motion Components.
              </span>
            </div>
            <div className="flex flex-1 w-full rounded-lg mt-4 bg-gradient-to-br from-violet-500 via-purple-500 to-blue-500" />
          </div>
        </PinContainer>
      </div>
      <HeroParallax products={products} />
      <TwoSectionComponent />
      <Contact />
      <Footer />
    </>
  );
};

export default LandingPage;
